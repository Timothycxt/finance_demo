from flask import Blueprint, jsonify

from App.models import simu_cacu
from App.models.corp_news import CorpNews

# （蓝图的名字，导入的名字）
corp_news = Blueprint('corp_news', __name__)


@corp_news.route('/corp_news', methods=['GET'])
def corp_news_list():
    res = CorpNews.query.all()
    data = []
    for item in res:
        data.append(item.to_json())
    return jsonify(data)


@corp_news.route('/corp_news/<id>', methods=['GET'])
def corp_by_id(id):
    corp_news = CorpNews.query.filter_by(id=id).first()
    res = {}
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = corp_news.to_json()
    return jsonify(res)


@corp_news.route('/corp_news/simu', method=['GET'])
def corp_news_simu():
    simu = simu_cacu.getData()
    res = {}
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = simu
    return jsonify(res)
