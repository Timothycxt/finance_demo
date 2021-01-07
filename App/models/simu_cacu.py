from datetime import datetime
import math

import jieba
from gensim import corpora, models, similarities
import codecs
from App.extensions import db
from App.models.corp_info import CorpInfo
from App.models.corp_news import CorpNews


# 查询新闻中的标题、公司、发布时间
def corp_news_list():
    from manager import app
    app_context = app.app_context()
    app_context.push()
    res = db.session.query(CorpNews.title, CorpNews.corporation, CorpNews.publish_date).all()
    data = []
    for item in res:
        # print(type(item), str(item[0]), str(item[1]), str(item[2]))
        data.append([str(item[0]), str(item[1]), item[2]])
    app_context.pop()
    return data


# 查询公司编号和名字
def corp_list():
    from manager import app
    app_context = app.app_context()
    app_context.push()
    res = db.session.query(CorpInfo.name, CorpInfo.id).all()
    data = {}
    for item in res:
        data.update({item[0]: item[1]})
    app_context.pop()
    return data


# 事件类描述词
corpus = [
    ['金融欺诈 ', '金融诈骗', '欺诈', '诈骗', '借壳', '借壳上市', '欺骗', '撒谎', '闪烁其词', '夸大宣传'],
    ['财务造假', '财务虚报', '财务谎报', '虚增营收', '虚增利息', '虚增营业利润'],
    ['欠税', '偷税', '漏税', '稽查', '上下游稽查', '限制高消费'],
    ['侵犯劳动者权益', '违犯劳动法律', '侵犯权益', '违反劳动合同', '侵犯权益', '不批准带薪假', '强制加班', '延长工时', '不签订劳务合同', '迟签订劳动合同', '罚没工资'],
    ['注册地更改', '注册地变更', '迁址', '召开会议', '审议', '通过议案', '领取新营业执照', '工商登记', '发布公告'],
    ['破坏企业系统', '破坏系统', '破坏数据库', '恶意删除数据', '删除数据库', '恶意修改数据'],
    ['员工贪污公款', '挪用公款', '携款逃跑', '贪污公款', '贪污，脏款，卷款', '受贿', '受到贿赂', '拿脏款', '移用', '挪用'],
    ['员工涉嫌贿赂', '贿赂', '行贿', '用财物买通别人'],
    ['产品质量不合格', '不合格', '不达标', '不符合相关标准', '安全隐患', '发布通告', '被通告', '被公告', '处罚', '警告', '罚款', '整改', '行政处理', '加强质量监督管理', '督促',
     '产品质量监督抽查', '抽检', '召回'],
    ['产品涉假', '标签违规', '虚假宣传', '停止宣传', '停止发布涉嫌虚假的信息', '停产', '整改', '处罚', '行政处罚'],
    ['产生矛盾', '存在争议', '冲突升级', '产生冲突', '存在争议', '不被看好', '矛盾激化', '冲突升级', '不和'],
    ['高层人员违法', '被举报', '移交司法机关', '违规', '违规', '涉嫌内部交易', '私自', '起诉', '被逮捕', '入狱', '被逮捕', '被拘留'],
    ['股东撤资', '清空股票', '套现走人', '股权转让', '撤资', '清空股票', '套现走人', '股权转让'],
    ['管理层内斗', '高层离职', '争斗控制权', '打压异己', '打压', '排挤', '罢免', '辞职', '离职', '离开', '清嫡', '管理层内斗', '内斗', '争夺控制权', '冲突升级'],
    ['股票套现', '减持股票', '抛售股票', '套现', '减持', '抛售'],
]
# 严重程度
dangerous = {0: 3, 1: 3, 2: 3, 3: 3, 4: 30, 5: 5, 6: 5, 7: 5, 8: 2, 9: 2, 10: 2, 11: 7, 12: 7, 13: 7, 14: 10}
# 事件按年月分类
event_group = {}
corp_score = {}
all_score = []


def init_corp_score(n_year):
    now_date = datetime.strptime('2020-12-31', '%Y-%m-%d')  # 当前时间，假定是2020-12-31
    # now_date = datetime.datetime.today()
    corp_group = corp_list()  # 公司name-code
    value = list(corp_group.values())
    for i in range(0, len(value)):
        corp_score.update({value[i]: {}})
        _id = corp_score.get(value[i])
        for year_num in range(0, n_year):
            _year = int(now_date.year) - year_num
            _id.update({_year: {}})
            __year = _id.get(_year)
            for month_num in range(1, 13):
                __year.update({month_num: []})


def event_bow():
    # 建立事件本体词袋模型
    dictionary = corpora.Dictionary(corpus)
    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    for text in corpus:
        print("text:", text)
    # print(len(doc_vectors), doc_vectors)
    #####################################################################
    # print(dictionary.num_docs)  # 文档数目
    # print(dictionary.num_pos)  # 所有词的个数
    # print(dictionary.dfs)  # 单词在文档中出现的次数
    # print(dictionary.id2token)  # 字典，{单词id:对应的词}
    # print(dictionary.token2id)  # 字典，{词:对应的单词id}
    # print(dictionary.num_nnz)  # 每个文件中不重复词个数的和
    ##########################################################################
    return dictionary, doc_vectors


# 分词、去停用词
def cut_words(news, stopwords):
    all_words = []
    for i in range(0, len(news)):
        words = jieba.lcut(''.join(news[i][0].split()))
        # print(len(words), words)
        res = drop_Disable_Words(words, stopwords)
        # print(len(res), type(res), res, res[0])
        all_words.append([res, news[i][1], news[i][2]])
    return all_words


# 去停用词
def drop_Disable_Words(cut_res, stopwords):
    res = []
    for word in cut_res:
        if word in stopwords or word == "\n" or word == "\u3000":
            continue
        res.append(word)
    # print(len(res), res)  # 查看去停用词结果
    return res


# 读取停用词
def read_stop_word(file_path):
    file = file_path
    stopwords = codecs.open(file, 'r', encoding='utf8').readlines()
    stopwords = [w.strip() for w in stopwords]
    return stopwords


# 计算相似度
def caculate(words, dictionary, doc_vectors):
    news_bow = dictionary.doc2bow(words[0])  # 建立新闻文本向量
    date = words[2]
    if len(news_bow) != 0:
        # print("words:", words)
        # print("news_bow:", news_bow)  # (x,y) ID为x的单词出现了y次

        tfidf = models.TfidfModel(doc_vectors)
        tfidf_vectors = tfidf[doc_vectors]
        # for i in range(0, len(tfidf_vectors)):
        #     print(len(tfidf_vectors[i]), tfidf_vectors[i])

        # 使用TF-IDF模型计算相似度
        TF_list = TF_IDF(tfidf_vectors, news_bow)
        # print("TF_IDF:", TF_list, '\n')
        event_class = 0  # 事件类
        confidence = 0  # 置信度
        # 取可信度最高的事件类
        for i in range(0, len(TF_list)):
            if confidence < TF_list[i][1]:
                confidence = TF_list[i][1]
                event_class = TF_list[i][0]
        return {"words": words[0], "corp_name": words[1], "news_date": words[2], "event_class": event_class,
                "confidence": confidence}  # [分词，公司名，时间，匹配事件类，可信度]
    # tfidf = models.TfidfModel(doc_vectors)
    # tfidf_vectors = tfidf[doc_vectors]
    # # for i in range(0, len(tfidf_vectors)):
    # #     print(len(tfidf_vectors[i]), tfidf_vectors[i])
    #
    # # 使用TF-IDF模型计算相似度
    # TF_list = TF_IDF(tfidf_vectors, news_bow)
    # # print("TF_IDF:", TF_list, '\n')
    # event_class = 0  # 事件类
    # confidence = 0  # 置信度
    # # 取可信度最高的事件类
    # for i in range(0, len(TF_list)):
    #     if confidence < TF_list[i][1]:
    #         confidence = TF_list[i][1]
    #         event_class = TF_list[i][0]
    # return {"words": words[0], "corp_name": words[1], "news_date": words[2], "event_class": event_class,
    #         "confidence": confidence}  # [分词，公司名，时间，匹配事件类，可信度]


# 建立TF-IDF模型
def TF_IDF(tfidf_vectors, news_bow):
    index = similarities.MatrixSimilarity(tfidf_vectors)
    sims = index[news_bow]
    return list(enumerate(sims))


def bulid():
    # 建立事件本体词袋模型
    dictionary, doc_vectors = event_bow()
    # 读取原始语料、停用词表
    news = corp_news_list()
    stopwords = read_stop_word("App/models/stopwords.txt")
    all_words = cut_words(news, stopwords)
    TF_list = []
    for words in all_words:
        result = caculate(words, dictionary, doc_vectors)  # [分词，公司名，时间，匹配事件类，可信度]
        if result is not None:
            # ######################################################
            # with open("负面事件.txt", 'a', encoding="utf8") as f:
            #     for i in result:
            #         f.write(''.join(str(i)) + " ")
            #     f.write('\n')
            # ######################################################
            TF_list.append(result)
    return TF_list


def get_target_date(n_year):
    now_date = datetime.strptime('2020-12-31', '%Y-%m-%d')  # 当前时间，假定是2020-12-31
    target_year = int(now_date.year) - n_year
    target_month = str(now_date.month)
    target_day = str(now_date.day)
    return now_date, target_year, target_month, target_day


def get_corp_score(event_recorder, _id, year, month):
    corp_id = corp_score.get(_id)
    score = 0.0
    for _num in range(0, len(corpus)):
        news_num = int(event_recorder.get(_num))
        # print("新闻数:" + str(news_num))
        if news_num > 1:
            score += math.log(news_num, 10) * dangerous.get(_num)
        elif news_num == 1:
            score += news_num * dangerous.get(_num)
        else:
            score += 0.0
    _year = corp_id.get(year)
    _month = _year.get(month)
    _month.append(score)
    return str(_id) + str(year) + str(month) + "已处理,分数:" + str(score)


def group_by_year(TF_list, n_year):
    corp_group = corp_list()  # 公司name-code
    value = list(corp_group.values())

    now_date, target_year, target_month, target_day = get_target_date(n_year)
    target_date = datetime.strptime(str(target_year) + '-' + target_month + '-' + target_day, '%Y-%m-%d')  # n年前的今天的日期
    for corp_id in value:
        event_group.update({corp_id: {}})
        _id = event_group.get(corp_id)
        for year_num in range(0, n_year):  # 创建n个年月二维列表，如果当前不是年底可以在今年后面的空缺月里补第一年多出的几个月，也可用新方法创建列表
            _year = int(now_date.year) - year_num
            _id.update({_year: {}})
            __year = _id.get(_year)
            for month_num in range(1, 13):
                __year.update({month_num: []})

    # 把事件按年月过滤、分类
    for item in TF_list:
        corp_id = corp_group.get(item['corp_name'])
        _corp = {}
        _year = {}
        _month = []
        if isinstance(item['news_date'], str):
            continue
            publist_date = datetime.strptime(item['news_date'], '%Y-%m-%d')
        else:
            publist_date = item['news_date']
        if publist_date > target_date and corp_id is not None:
            _corp = event_group.get(corp_id)
            _year = _corp.get(int(item['news_date'].year))
            _month = _year.get(int(item['news_date'].month))
            _month.append(item)
        # event_group.get(_corp).get(int(item['news_date'].year)).update({int(item['news_date'].month): _month})

    return event_group


def analysis(n_year):
    init_corp_score(n_year)  # 初始化corp_score
    TF_list = bulid()  # 语义匹配数据
    group_by_year(TF_list, n_year)  # 事件分类函数
    now_date, target_year, target_month, target_day = get_target_date(n_year)  # 获取时间范围

    for item in event_group:
        _corp = event_group.get(item)  # 事件类的公司列表
        for year_num in range(0, n_year):
            _year = int(now_date.year) - year_num
            __year = _corp.get(_year)  # 该公司事件的年列表
            for month_num in range(1, 13):
                _month = __year.get(month_num)  # 该公司一年事件的月列表
                event_recorder = {}  # 单个公司每月的新闻记录
                for i in range(0, len(corpus)):  # 初始化事件记录列表(15条)
                    event_recorder.update({i: 0})
                for _month_item in _month:  # 一个月中的单个事件
                    # print(_month_item)
                    if event_recorder.get(_month_item["event_class"]) is not None:  # 发生了某类事件且事件已被记录
                        # print(event_recorder.get(_month_item["event_class"]), item, _year, month_num)
                        event_recorder.update({_month_item["event_class"]: event_recorder.get(
                            _month_item["event_class"]) + 1})  # 更新{事件： 数量+1}
                    else:  # 发生了某类事件且事件未被记录
                        # print(item, _year, month_num)
                        event_recorder.update({_month_item["event_class"]: 1})
                response = get_corp_score(event_recorder, item, _year, month_num)  # 将一个月的事件送去处理打分
                # print(response)

    influence_corp_score = {}  # 受上个月影响的本月分数
    pre_score = 0
    # 逐层创建影响系数分数列表，并且读取原始扣分列表
    for item in corp_score:  # 第一层公司代码列表
        influence_corp_score.update({item: {}})
        _corp_i = influence_corp_score.get(item)
        _corp = corp_score.get(item)
        for year_num in range(0, n_year):  # 第二层年份列表
            _year = int(now_date.year) - year_num
            _corp_i.update({_year: {}})
            __year_i = _corp_i.get(_year)
            __year = _corp.get(_year)
            for month_num in range(1, 13):  # 第三层月份列表
                # __year_i.update({month_num: []})
                # _month_i = __year_i.get(month_num)
                # _month = __year.get(month_num)
                # _month_i.append(100 - pre_score * 0.13 - _month[0])
                # pre_score = _month[0]
                _month = __year.get(month_num)
                __year_i.update({month_num: 100 - pre_score * 0.13 - _month[0]})
                pre_score = _month[0]
    return influence_corp_score


def getData(_id):
    _data = all_score
    if not all_score:
        _data = analysis(3)
    _corpus = _data.get(int(_id))  # 获取某个公司的数据
    now_date = datetime.strptime('2020-12-31', '%Y-%m-%d')  # 当前时间，假定是2020-12-31
    # now_date = datetime.datetime.today()
    _scores = []
    for year_num in range(0, 3):
        target_year = int(now_date.year) - year_num
        _year = _corpus.get(target_year)
        _scores.append({"label": target_year, "data": list(_year.values())})
    print(_scores)
    return_data = {
        "id": _id,
        "datasets": _scores
    }
    return return_data

# if __name__ == "__main__":
#     getData(1)
