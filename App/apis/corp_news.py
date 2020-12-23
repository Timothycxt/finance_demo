from flask import Blueprint, jsonify
from App.models import simu_cacu
from flask_paginate import Pagination, request, get_page_parameter
from App.models.corp_news import CorpNews

corp_news = Blueprint('corp_news', __name__)


# 所有新闻的展示列表,每页10条新闻标题
@corp_news.route('/corp_news/<page>/<pre_page>', methods=['GET'])
def corp_news_list(page, pre_page):
    page = int(page)
    pre_page = int(pre_page)
    total = CorpNews.query.count()
    start = (page - 1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    corp_news_list = CorpNews.query.order_by(CorpNews.publish_date.desc()).slice(start, end)

    items = []
    data = {}
    res = {}
    for corp_new in corp_news_list:
        tmp = corp_new.to_json()
        time = str(tmp['publish_date'])
        tmp = {
            'id': tmp['id'],
            'title': tmp['title'],
            'link': tmp['link'],
            'emotion': tmp['emotion_trend'],
            'keywords': tmp['keywords'],
            'publish_date': time
        }
        items.append(tmp)
    data['items'] = items
    data['total'] = total

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)


# 展示一家企业新闻列表,每页10条新闻
@corp_news.route('/corp_news/<corporation>/<page>/<pre_page>', methods=['GET'])
def corp_by_name(corporation, page, pre_page):
    page = int(page)
    pre_page = int(pre_page)

    total = CorpNews.query.filter(CorpNews.corporation == corporation).count()
    start = (page - 1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    corp_news = CorpNews.query.filter(CorpNews.corporation == corporation).order_by(CorpNews.publish_date.desc()).slice(
        start, end)

    items = []
    data = {}
    res = {}

    for corp_new in corp_news:
        tmp = corp_new.to_json()
        tmp = {
            'id': tmp['id'],
            'title': tmp['title'],
            'link': tmp['link'],
            'emotion': tmp['emotion_trend'],
            'keywords': tmp['keywords']
        }
        items.append(tmp)
    data['total'] = total
    data['items'] = items

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)


@corp_news.route('/corp_news/simu', methods=['GET'])
def corp_news_simu():
    simu = simu_cacu.getData()
    res = {}
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = simu
    return jsonify(res)
