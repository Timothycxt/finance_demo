from App.dao.MySql.industry_news import get_recent_news
import jieba.analyse
import os
# import pyecharts.options as opts
# from pyecharts.charts import WordCloud
# from pyecharts.globals import SymbolType


# 根据行业最近新闻返回热点词及其词频
# parameters:
#   industry: 行业名称
# returns:
#     [
#         # 热点词和词频
#         {
#             "name": "生物",
#             "value": 1.0
#         },
#         ...
#     ]
def get_keywords(industry):
    news = get_recent_news(industry)
    text = ' '.join(news)
    print('text length:', len(text))

    dirpath = os.path.dirname(os.path.realpath(__file__))
    STOP_WORDS_FILE_PATH = os.path.join(dirpath, '../models/stopwords.txt')
    jieba.analyse.set_stop_words(STOP_WORDS_FILE_PATH)

    # 词数统计
    words_count_list = jieba.analyse.textrank(text, topK=50, withWeight=True)
    # words_count_list = jieba.analyse.extract_tags(text, topK=50, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    # 函数：jieba.analyse.textrank(string, topK=20, withWeight=True, allowPOS=())
    # string：待处理语句
    # topK：关键字的个数，默认20
    # withWeight：是否返回权重值，默认false
    # allowPOS：是否仅返回指定类型，默认为空

    print(words_count_list)
    print(len(words_count_list))  # 50

    # 生成词云
    # word_cloud = (WordCloud().add("", words_count_list, word_size_range=[20, 100], shape=SymbolType.DIAMOND).
    #               set_global_opts(title_opts=opts.TitleOpts(title="CSV2WC Test")))
    # word_cloud.render(os.path.join(dirpath, 'Word_Cloud_CSV.html'))

    res = [{'name': name, 'value': value} for name, value in words_count_list]
    return res
