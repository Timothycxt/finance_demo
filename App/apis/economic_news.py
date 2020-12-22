from flask import Blueprint
from flask import jsonify
from App.models.economic_news import EconomicNews

economic_new = Blueprint('economic_news', __name__)


@economic_new.route('/economic_news', methods=['GET'])
def economic_news():
    economic_news = EconomicNews.query.all()
    data = []
    res = {}  # 返回一个字典，包含状态码，信息，数据
    for item in economic_news:
        data.append(item.to_json())
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)
