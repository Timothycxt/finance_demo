import jieba
import simplejson
from flask import jsonify
from gensim import corpora, models, similarities
import codecs

from App.models.corp_news import CorpNews


def corp_news_list():
    res = CorpNews.query.all()
    data = []
    for item in res:
        data.append(item.to_json())
    print(data)
    return jsonify(data)


def event_bow():
    corpus = [
        ['金融欺诈 ', '金融诈骗', '欺诈', '诈骗', '借壳', '借壳上市', '欺骗', '撒谎', '闪烁其词', '夸大宣传'],
        ['财务造假', '财务虚报', '财务谎报', '虚增营收', '虚增利息', '虚增营业利润'],
        ['欠税', '偷税', '漏税', '稽查', '上下游稽查', '限制高消费'],
        ['侵犯劳动者权益', '违犯劳动法律', '侵犯权益', '违反劳动合同', '侵犯权益', '不批准带薪假', '强制加班', '延长工时', '不签订劳务合同', '迟签订劳动合同', '罚没工资'],
        ['注册地更改', '注册地变更', '迁址', '召开会议', '审议', '通过议案', '领取新营业执照', '工商登记', '发布公告'],
        ['破坏企业系统', '破坏系统', '破坏数据库', '恶意删除数据', '删除数据库', '恶意修改数据'],
        ['员工贪污公款', '挪用公款', '携款逃跑', '贪污公款', '贪污，脏款，卷款', '受贿', '受到贿赂', '拿脏款', '移用', '挪用'],
        ['员工涉嫌贿赂', '贿赂', '行贿', '用财物买通别人'],
        ['产品质量不合格', '不合格', '不达标', '不符合相关标准', '安全隐患', '发布通告', '被通告', '被公告', '处罚', '警告', '罚款', '整改', '行政处理', '加强质量监督管理',
         '督促', '产品质量监督抽查', '抽检', '召回'],
        ['产品涉假', '标签违规', '虚假宣传', '停止宣传', '停止发布涉嫌虚假的信息', '停产', '整改', '处罚', '行政处罚'],
        ['产生矛盾', '存在争议', '冲突升级', '产生冲突', '存在争议', '不被看好', '矛盾激化', '冲突升级', '不和'],
        ['高层人员违法', '被举报', '移交司法机关', '违规', '违规', '涉嫌内部交易', '私自', '起诉', '被逮捕', '入狱', '被逮捕', '被拘留'],
        ['股东撤资', '清空股票', '套现走人', '股权转让', '撤资', '清空股票', '套现走人', '股权转让'],
        ['管理层内斗', '高层离职', '争斗控制权', '打压异己', '打压', '排挤', '罢免', '辞职', '离职', '离开', '清嫡', '管理层内斗', '内斗', '争夺控制权', '冲突升级'],
        ['股票套现', '减持股票', '抛售股票', '套现', '减持', '抛售'],
    ]
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


def cut_words(news, stopwords):
    # 分词、去停用词
    all_words = []
    # for file in files:
    #     with open(file, 'r', encoding="utf-8") as f:
    #         lines = f.readlines()
    #         for line in lines:
    #             js = simplejson.loads(line)
    #             words = jieba.lcut(''.join(js["title"].split()))  # cut生成一个生成器，通过for来取得其中的内容，lcut直接获得一个列表
    #             # print(len(words), words)
    #             # 去停用词
    #             res = drop_Disable_Words(words, stopwords)
    #             all_words.append(res)
    #             # print(len(res), type(res), res, res[0])
    # return all_words
    for new in news:
        words = jieba.lcut(''.join(new['title'].split()))
        print(len(words), words)
        res = drop_Disable_Words(words, stopwords)
        # print(len(res), type(res), res, res[0])
        all_words.append(res)
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
    # words = numpy.array(res).reshape(len(res), 1)
    # print("words:", words)

    # 建立新闻文本向量
    # print(words)
    news_bow = dictionary.doc2bow(words)
    if len(news_bow) != 0:
        print("words:", words)
        print("news_bow:", news_bow)  # (x,y) ID为x的单词出现了y次

        tfidf = models.TfidfModel(doc_vectors)
        tfidf_vectors = tfidf[doc_vectors]
        # print(len(tfidf_vectors))
        # for i in range(0, len(tfidf_vectors)):
        #     print(len(tfidf_vectors[i]), tfidf_vectors[i])

        # # 使用LSI模型计算相似度
        # LSI_list = LSI(tfidf_vectors, dictionary, doc_vectors, 5)
        # # print("LSI:", LSI_list)
        # for i in LSI_list:
        #     list_i = i[1].tolist()
        #     print(list_i)
        #     print(list_i.index(max(list_i)))

        # 使用TF-IDF模型计算相似度
        TF_list = TF_IDF(tfidf_vectors, news_bow)
        print("TF_IDF:", TF_list)
        return TF_list


# 建立TF-IDF模型
def TF_IDF(tfidf_vectors, news_bow):
    index = similarities.MatrixSimilarity(tfidf_vectors)
    sims = index[news_bow]
    return list(enumerate(sims))


# 建立LSI模型
def LSI(tfidf_vectors, dictionary, news_bow, theme_num):
    # lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=theme_num)
    # lsi_vector = lsi[tfidf_vectors]
    # query_lsi = lsi[news_bow]
    # index = similarities.MatrixSimilarity(lsi_vector)
    # sims = index[query_lsi]
    # return list(enumerate(sims))
    lsi = models.LsiModel(news_bow, id2word=dictionary, num_topics=theme_num)
    lsi_vector = lsi[news_bow]
    query_lsi = lsi[tfidf_vectors]
    index = similarities.MatrixSimilarity(lsi_vector)
    sims = index[query_lsi]
    return list(enumerate(sims))


def main():
    # 建立事件本体词袋模型
    dictionary, doc_vectors = event_bow()
    # 读取原始语料、停用词表
    files = ['C:\\Users\\LiYanhao\\Desktop\\Something\\Reptile\\Data\\联合汽车电子有限公司.txt',
             ]
    news = corp_news_list()
    stopwords = read_stop_word("stopwords.txt")
    all_words = cut_words(news, stopwords)
    TF_list = []
    for words in all_words:
        TF_list.append(caculate(words, dictionary, doc_vectors))
    return TF_list


if __name__ == "__main__":
    main()