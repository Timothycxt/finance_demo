from App.models.indu_news import Indu_news


# 查询行业最近新闻
def get_recent_news(industry):
    news = Indu_news.query.filter(Indu_news.industy == industry, Indu_news.content != '').limit(20)

    rs = []
    for item in news:
        data = item.to_json()
        tmp = data['content']
        rs.append(tmp)

    print(f'get {len(rs)} recently news')
    # for i in rs[:10]:
    #     print(i)
    return rs
