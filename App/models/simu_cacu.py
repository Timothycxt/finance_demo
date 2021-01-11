from datetime import datetime
import math
import jieba
from gensim import corpora, models, similarities
import codecs
from App.extensions import db
from App.models.corp_info import CorpInfo
from App.models.corp_news import CorpNews
from App.models.corp_score import Corp_score


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
    res = db.session.query(CorpInfo.name, CorpInfo.code).all()
    data = {}
    for item in res:
        data.update({item[0]: item[1]})
    app_context.pop()
    return data


# 按公司编号存储/更新分数
def score_to_database(_code, _scores):
    from manager import app
    app_context = app.app_context()
    app_context.push()
    _exist = Corp_score.query.filter_by(code=_code).first()
    if _exist is not None:
        Corp_score.query.filter_by(code=_code).update({'score': _scores})
        res = "Already Update"
        print("Update")
    else:
        _corp_score = Corp_score(code=_code, score=_scores)
        db.session.add(_corp_score)
        db.session.commit()
        res = "Already Add"
        print("Add")
    app_context.pop()
    return res


# 按公司编号查询分数
def search_score_by_code(_code):
    from manager import app
    app_context = app.app_context()
    app_context.push()
    _score = Corp_score.query.filter_by(code=_code).first()
    app_context.pop()
    return _score.score


# 事件类描述词
corpus = [
    ['金融欺诈', '金融诈骗', '欺诈', '诈骗', '借壳', '借壳上市', '欺骗', '撒谎', '闪烁其词', '夸大宣传'], # 金融欺诈
    ['财务造假', '财务虚报', '财务谎报', '虚增营收', '虚增利息', '虚增营业利润'], # 财务造假
    ['欠税', '偷税', '漏税', '稽查', '上下游稽查', '限制高消费'], # 企业税务
    ['侵犯劳动者权益', '违犯劳动法律', '侵犯权益', '违反劳动合同', '侵犯权益', '不批准带薪假', '强制加班', '延长工时', '不签订劳务合同', '迟签订劳动合同', '罚没工资'], # 企业侵犯劳动者权益
    ['注册地更改', '注册地变更', '迁址', '召开会议', '审议', '通过议案', '领取新营业执照', '工商登记', '发布公告'], # 企业注册地更改
    ['破坏企业系统', '破坏系统', '破坏数据库', '恶意删除数据', '删除数据库', '恶意修改数据'], # 破坏企业系统
    ['员工贪污公款', '挪用公款', '携款逃跑', '贪污公款', '贪污，脏款，卷款', '受贿', '受到贿赂', '拿脏款', '移用', '挪用'], # 员工贪污
    ['员工涉嫌贿赂', '贿赂', '行贿', '用财物买通别人'], # 员工行贿
    ['产品质量不合格', '不合格', '不达标', '不符合相关标准', '安全隐患', '发布通告', '被通告', '被公告', '处罚', '警告', '罚款', '整改', '行政处理', '加强质量监督管理', '督促',
     '产品质量监督抽查', '抽检', '召回'], # 产品质量不合格
    ['产品涉假', '标签违规', '虚假宣传', '停止宣传', '停止发布涉嫌虚假的信息', '停产', '整改', '处罚', '行政处罚'], # 产品涉假
    ['产生矛盾', '存在争议', '冲突升级', '产生冲突', '存在争议', '不被看好', '矛盾激化', '冲突升级', '不和'], # 股东不和
    ['高层人员违法', '被举报', '移交司法机关', '违规', '违规', '涉嫌内部交易', '私自', '起诉', '被逮捕', '入狱', '被逮捕', '被拘留'], # 高层违法
    ['股东撤资', '清空股票', '套现走人', '股权转让', '撤资', '清空股票', '套现走人', '股权转让'], # 股东撤资
    ['管理层内斗', '高层离职', '争斗控制权', '打压异己', '打压', '排挤', '罢免', '辞职', '离职', '离开', '清嫡', '管理层内斗', '内斗', '争夺控制权', '冲突升级'], # 管理层争权
    ['股票套现', '减持股票', '抛售股票', '套现', '减持', '抛售'], # 股票套现
    ['企业迁移', '公司搬迁', '公司注册地变更', '经营地址变更', '税务迁移', '迁入地税务局', '迁出地税务局', '搬迁', '迁往', '搬离', '搬到', '迁至',
     '迁移', '逃离浦东', '逃离上海', '经营地址变更', '公司变更登记申请书', '领取营业执照', '企业注册地更改', '移送企业登记档案通知函', '关于迁至变更登记的通知',
     '工商资料转出手续', '企业迁出核准通知书', '工商执照迁移', '迁出地营业执照', '迁出地工商局', '工商准许迁出通知书', '迁入地工商局', '迁入地营业执照'], # 企业迁移
    ['产值变化', '产值瓶颈', '产值下滑', '产值负增长', '产值下降', '同比下降', '市场走低', '上游订单减少'], # 产值变化
    ['销售变化', '销售下滑', '销售下降', '销量下降', '销量下滑', '销售停滞', '签单停滞', '业务停顿'], # 销售变化
    ['部门调整', '重新规划部门职能', '部门调整', '合并业务', '部门业务变更', '关闭部门 '], # 部门调整
    ['高层引咎辞职', '高层离职', '解除劳动合同', '约谈', '引咎辞职', '决策失误 '], # 高层引咎辞职
    ['削减人员配置', '裁员', '减少员工人数', '离职'], # 削减人员配置
    ['股价下跌', '股价跳水', '股价创新低', '换手', '抛售', '收盘', '市值蒸发', '市值降低', '跌停', '崩盘'], # 股价下跌
    ['企业负债', '企业欠款', '背负债务', '并购', '市值蒸发', '利益增速下降', '营收下降', '质押股权', '分裂', '拆分子公司', '负债率超标', '负债率踩线', '资金流失', '现金流锐减'], # 企业负债
    ['营业收入下降', '交付额下降', '销售额降低', '同比下降', '低于去年', '低于同时期', '公布财报', '负债', '欠款', '负债率', ' 销量减少', '销售额减少', '实现营业收入', '营收总额'], # 营业收入下降
    ['资产剥离', '剥离股权', '资产出售', '股权出售', '资产分离'], # 资产剥离
    ['收购兼并', '公司收购', '公司兼并重组', '兼并重组', '兼并', '合并', '重组', '重构', '收购资产', '收购', '并购资产', '合并资产'], # 收购兼并
    ['资产置换', '资产互换', '资产换入', '资产换出', '股权互换', '股权交换', '债权互换', '债权交换'], # 资产置换
    ['股权转让', '公司股权转让', '股份转让', '股权拍卖', '股份拍卖', '购并', '流通股购并', '股权购并', '股份购并', '股权合并', '划拨', '非流通股划拨', '非流通股划拨', '非流通股划拨'] # 股权转让
]
# 事件类-id映射
id2event = [item[0] for item in corpus]
event2id = {id2event[i]: i for i in range(len(id2event))}

# 严重程度
dangerous = {0: 3, 1: 3, 2: 3, 3: 3, 4: 30, 5: 5, 6: 5, 7: 5, 8: 2, 9: 2, 10: 2, 11: 7, 12: 7, 13: 7, 14: 10, 15: 30, 16: 10, 17: 10, 18: 3, 19: 3, 20: 3, 21: 7, 22: 10, 23: 5, 24: 10, 25: 3, 26: 3, 27: 3, 28: 5}
# 事件按年月分类
# 字典 公司id:年份dict
# 年份dict 年份:月份dict
# 月份dict 月份:事件类匹配结果list
event_group = {}

# 企业扣分分数
corp_score = {}

# 处理后返回给前端的分数
all_score = []


# 初始化corp_score数据格式
def init_corp_score(n_year):
    now_date = datetime.strptime('2020-12-31', '%Y-%m-%d')  # 当前时间，假定是2020-12-31
    # now_date = datetime.today()
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


# 建立事件本体词袋模型
def event_bow():
    dictionary = corpora.Dictionary(corpus)  # 建立词典
    doc_vectors = [dictionary.doc2bow(text) for text in corpus]  # 每条文本转为向量，词语对应词典中的index
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
        res = drop_Disable_Words(words, stopwords)
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


def caculate(words, dictionary, doc_vectors):
    """
    计算新闻与所有事件类的相似度
    :param words: 一条分词后的新闻 [['豪华', '务实', '奥迪', 'Q3', '静态', '凯迪拉克', 'XT4'], '上汽通用汽车有限公司', datetime.datetime(2020, 12, 3, 0, 0)]
    :param dictionary: 事件类的词典
    :param doc_vectors:
    :return:
    """
    news_bow = dictionary.doc2bow(words[0])  # 建立新闻文本向量
    # 新闻中没有事件类相关的单词则丢弃
    if len(news_bow) != 0:
        # print("words:", words)
        # print("news_bow:", news_bow)  # (x,y) ID为x的单词出现了y次

        tfidf = models.TfidfModel(doc_vectors)
        tfidf_vectors = tfidf[doc_vectors]

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


# 建立TF-IDF模型
def TF_IDF(tfidf_vectors, news_bow):
    index = similarities.MatrixSimilarity(tfidf_vectors)
    sims = index[news_bow]
    return list(enumerate(sims))


# 筛选有价值的新闻
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
        # 新闻中没有事件类相关的单词则返回空，丢弃
        if result is not None:
            TF_list.append(result)
    return TF_list


# 获取计算起始年份
def get_target_date(n_year):
    now_date = datetime.strptime('2020-12-31', '%Y-%m-%d')  # 当前时间，假定是2020-12-31
    target_year = int(now_date.year) - n_year
    target_month = str(now_date.month)
    target_day = str(now_date.day)
    return now_date, target_year, target_month, target_day


# 新闻扣分
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


# 把新闻按年月区分
def group_by_year(TF_list, n_year):
    corp_group = corp_list()  # 字典 公司name：id
    value = list(corp_group.values())
    now_date, target_year, target_month, target_day = get_target_date(n_year)
    target_date = datetime.strptime(str(target_year) + '-' + target_month + '-' + target_day, '%Y-%m-%d')  # n年前的今天的日期
    for corp_id in value:
        event_group.update({corp_id: {}})  # event_group存储事件按年月分类结果
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
        else:
            publist_date = item['news_date']
        if publist_date > target_date and corp_id is not None:
            _corp = event_group.get(corp_id)
            _year = _corp.get(int(item['news_date'].year))
            _month = _year.get(int(item['news_date'].month))
            _month.append(item)

    # return event_group


# 把group_by_year区分好的数据按事件类型区分处理，处理好的数据送入get_corp_score扣分后再生成最终的企业分数
def analysis(n_year):
    """

    :param n_year: 根据最近几年的数据进行分析
    :return:
    """
    init_corp_score(n_year)  # 初始化corp_score
    # 所有公司新闻与所有事件类的相似度匹配结果
    # {'words': ['美国', '新造', '车', '公司', '陷', '欺诈', '风波', '通用', '放弃', '持股', '计划'], 'corp_name': '上汽通用汽车有限公司', 'news_date': datetime.datetime(2020, 12, 3, 0, 0), 'event_class': 0, 'confidence': 0.31622776}
    TF_list = bulid()
    group_by_year(TF_list, n_year)  # 将匹配结果根据年份分类
    now_date, target_year, target_month, target_day = get_target_date(n_year)  # 获取时间范围
    # 处理每一个公司
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
                    if event_recorder.get(_month_item["event_class"]) is not None:  # 发生了某类事件且事件已被记录
                        event_recorder.update({_month_item["event_class"]: event_recorder.get(
                            _month_item["event_class"]) + 1})  # 更新{事件： 数量+1}
                    else:  # 发生了某类事件且事件未被记录
                        event_recorder.update({_month_item["event_class"]: 1})
                response = get_corp_score(event_recorder, item, _year, month_num)  # 将一个月的事件送去处理打分

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
                _month = __year.get(month_num)
                __year_i.update({month_num: 100 - pre_score * 0.13 - _month[0]})  # 给本月打分
                pre_score = _month[0]
    return influence_corp_score


def score_update():
    """
    计算所有企业各月份得分，返回前端需要的格式
    :param _id:
    :return:
    """
    # all_score存储计算结果，如果之前计算过则无需重复计算
    _data = all_score
    if not all_score:
        _data = analysis(3)  # 所有企业id和企业得分的映射，企业得分是年份与月份得分的映射，月份得分是月份与得分的映射

    _corp_id = list(corp_list().values())
    for _id in _corp_id:
        _corpus = _data.get(str(_id))  # 根据id获取某个公司的得分数据
        now_date = datetime.strptime('2020-12-31', '%Y-%m-%d')  # 当前时间，假定是2020-12-31
        # now_date = datetime.datetime.today()
        _scores = []
        for year_num in range(0, 3):
            target_year = int(now_date.year) - year_num
            _year = _corpus.get(target_year)  # 根据年份获取该公司的得分数据
            source = [[id2event[item['event_class']] for item in month] for month in
                      event_group[str(_id)][target_year].values()]
            source = [list(set(month)) for month in source]
            _scores.append({"label": target_year, "data": list(_year.values()), "source": source})
            print(_scores)
        _scores2str = str(_scores)
        score_to_database(_id, _scores2str)
    return "OK"


def getData(_code):
    _score = search_score_by_code(str(_code))
    print(_score)
    _score = eval(_score)
    return_data = {
        "id": _code,
        "datasets": _score
    }
    return return_data
    # if __name__ == "__main__":
    #     getData(1)
