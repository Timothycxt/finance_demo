from flask import Blueprint, jsonify
from App.models import simu_cacu
from flask_paginate import Pagination
from App.models.corp_news import CorpNews
from sqlalchemy import func

corp_news = Blueprint('corp_news', __name__)


@corp_news.route('/corp_news', methods=['GET'])
def corp_news_list():
    corp_news = CorpNews.query.all()
    data = []
    res={}
    for item in corp_news:
        data.append(item.to_json())
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)


@corp_news.route('/corp_news/<corporation>', methods=['GET'])
def corp_by_name(corporation):
    corp_news = CorpNews.query.filter_by(corporation=corporation).all()
    res = {}
    data=[]
    for corp_new in corp_news:
        data.append(corp_new.to_json())
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


@corp_news.route('/corp_news/numbers/<corporation>',methods=['GET'])
def corp_news_numbers(corporation):
    count_positive=CorpNews.query.filter(CorpNews.corporation==corporation,CorpNews.emotion_trend==1).count()
    count_middle=CorpNews.query.filter(CorpNews.corporation==corporation,CorpNews.emotion_trend==0).count()
    count_negative=CorpNews.query.filter(CorpNews.corporation==corporation,CorpNews.emotion_trend==-1).count()
    data=[count_positive,count_middle,count_negative]
    res={}
    res['status']=200
    res['msg']='请求成功'
    res['data']=data
    return jsonify(res)