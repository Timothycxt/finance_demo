import json

from flask import Blueprint, jsonify
from App.models.corp_info import CorpInfo

# （蓝图的名字，导入的名字）
blue = Blueprint('blue', __name__)


@blue.route('/corp/add', methods=['POST'])
def addCorp():
    corpInfo = CorpInfo()
    corpInfo.name = "test"
    corpInfo.save()
    return 'res'


@blue.route('/corp', methods=['GET'])
def corp_list():
    corp_list = CorpInfo.query.all()
    data = []
    res = {}  # 返回一个字典，包含状态码，信息，数据
    for item in corp_list:
        data.append(item.to_json())
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)


@blue.route('/corp/<id>', methods=['GET'])
def corp_by_id(id):
    corp = CorpInfo.query.filter_by(id=id).first()
    res = {}
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = corp.to_json()
    return jsonify(res)
