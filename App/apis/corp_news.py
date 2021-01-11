from flask import Blueprint, jsonify
from sqlalchemy import and_

from App.models import simu_cacu
from flask_paginate import Pagination, request, get_page_parameter

from App.models.corp_info import CorpInfo
from App.models.corp_news import CorpNews

corp_news = Blueprint('corp_news', __name__)


# 所有新闻的展示列表,每页10条新闻标题
@corp_news.route('/corp_news/page/<page>/<pre_page>', methods=['GET'])
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
        time = time[0:10]
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
@corp_news.route('/corp_news/page/<code>/<page>/<pre_page>', methods=['GET'])
def corp_by_name(code, page, pre_page):
    page = int(page)
    pre_page = int(pre_page)

    total = CorpNews.query.outerjoin(CorpInfo, CorpNews.corporation == CorpInfo.name).filter(
        CorpInfo.code == code).count()
    start = (page - 1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    corp_news = CorpNews.query.outerjoin(CorpInfo, CorpNews.corporation == CorpInfo.name).filter(
        CorpInfo.code == code).slice(start, end)

    items = []
    data = {}
    res = {}

    for corp_new in corp_news:
        tmp = corp_new.to_json()
        time = str(tmp['publish_date'])
        time = time[0:10]
        tmp = {
            'id': tmp['id'],
            'title': tmp['title'],
            'link': tmp['link'],
            'emotion': tmp['emotion_trend'],
            'keywords': tmp['keywords'],
            'publish_date': time
        }
        items.append(tmp)
    data['total'] = total
    data['items'] = items

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)


# 一家公司的新闻的情感倾向分别之和
@corp_news.route('/corp_news/emotion/<NSRSBM>/<NSRMC>/<SSXDM>', methods=['GET'])
def emotion(NSRSBM, NSRMC, SSXDM):
    total = CorpNews.query.outerjoin(CorpInfo, CorpNews.corporation == CorpInfo.name).filter(
        CorpInfo.code == NSRSBM, CorpInfo.name == NSRMC)

    positive = CorpNews.query.outerjoin(CorpInfo, CorpNews.corporation == CorpInfo.name).filter(
        CorpInfo.code == NSRSBM, CorpInfo.name == NSRMC).filter(CorpNews.emotion_trend == str(1)).count()

    middle = CorpNews.query.outerjoin(CorpInfo, CorpNews.corporation == CorpInfo.name).filter(
        CorpInfo.code == NSRSBM, CorpInfo.name == NSRMC).filter(CorpNews.emotion_trend == str(0)).count()

    negative = CorpNews.query.outerjoin(CorpInfo, CorpNews.corporation == CorpInfo.name).filter(
        CorpInfo.code == NSRSBM, CorpInfo.name == NSRMC).filter(CorpNews.emotion_trend == str(-1)).count()

    emotion = {
        'positive': positive,
        'middle': middle,
        'negative': negative
    }
    data = {}
    res = {}

    data['emotion'] = emotion
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)


@corp_news.route('/corp_news/simu/<_id>', methods=['GET'])
def corp_news_simu(_id):
    score = simu_cacu.getData(_id)
    res = {}
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = score
    return jsonify(res)
