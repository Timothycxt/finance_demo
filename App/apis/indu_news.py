from flask import Blueprint
from flask import jsonify
from flask_paginate import Pagination,get_page_parameter,request
from App.models.indu_news import Indu_news

indu_new = Blueprint('indu_news', __name__)

# 展示行业新闻,每页展示10条
@indu_new.route('/indu_news/<page>/<pre_page>',methods=['GET'])
def indu_news(page,pre_page):
    page = int(page)
    pre_page = int(pre_page)

    total = Indu_news.query.count()
    start = (page - 1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    indu_news_list= Indu_news.query.slice(start, end)

    res = {}
    data = []
    data.append({'total': total})

    for corp in indu_news_list:
        tmp=corp.to_json()
        tmp={
            'title':tmp['title'],
            'link':tmp['link'],
            'publish_date':tmp['publish_date'],
            'industry':tmp['industy'],
            'keywords':tmp['keywords']
        }
        data.append(tmp)

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)