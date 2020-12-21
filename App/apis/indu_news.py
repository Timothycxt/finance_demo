from flask import Blueprint
from flask import jsonify
from App.models.indu_news import Indu_news

indu_news = Blueprint('indu_news', __name__)

@indu_news.route('/indu_news',methods=['GET'])
def economic_news():
    indu_news=Indu_news.query.all()
    data = []
    res = {}  # 返回一个字典，包含状态码，信息，数据
    for item in indu_news:
        data.append(item.to_json())
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)