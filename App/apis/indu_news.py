from flask import Blueprint
from flask import jsonify
from flask_paginate import Pagination

from App.models.indu_news import Indu_news

indu_news = Blueprint('indu_news', __name__)


@indu_news.route('/indu_news/<page>/<pre_page>', methods=['GET'])
def indu_new(page,pre_page):
    page = int(page)
    pre_page = int(pre_page)

    total = Indu_news.query.count()
    start = (page - 1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    corp_list = Indu_news.query.slice(start, end)

    items=[]
    res = {}
    data = {}

    for corp in corp_list:
        tmp = corp.to_json()
        time=str(tmp['publish_date'])
        tmp = {
            'id':['id'],
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