from flask import Blueprint
from flask import jsonify
from flask_paginate import Pagination

from App.models.indu_news import Indu_news
from App.service.WordCloud import get_keywords

indu_news = Blueprint('indu_news', __name__)


@indu_news.route('/indu_news/<page>/<pre_page>', methods=['GET'])
def indu_new(page,pre_page):
    page = int(page)
    pre_page = int(pre_page)

    total = Indu_news.query.count()
    start = (page - 1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    corp_list = Indu_news.query.order_by(Indu_news.publish_date.desc()).slice(start, end)

    items=[]
    res = {}
    data = {}

    for corp in corp_list:
        tmp = corp.to_json()
        time=str(tmp['publish_date'])
        tmp = {
            'id':tmp['id'],
            'title': tmp['title'],
            'source': tmp['source'],
            'link': tmp['link'],
            'publishDate':time,
            'industy':tmp['industy']
        }
        items.append(tmp)
    data['total']=total
    data['items']=items

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)

# 获取行业词云所需的词频
@indu_news.route('/indu_news/keywords/<industry>', methods=['GET', 'POST'])
def _get_keywords(industry):
    industry = str(industry).strip()
    print(industry)

    res = {'status': 200, 'msg': '请求成功', 'data': {'defaultWords': get_keywords(industry)}}

    return jsonify(res)