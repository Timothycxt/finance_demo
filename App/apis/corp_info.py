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
    res = CorpInfo.query.all()
    data = []
    for item in res:
        data.append(item.to_json())
    return jsonify(data)


@blue.route('/corp/<id>', methods=['GET'])
def corp_by_id(id):
    res = CorpInfo.query.filter_by(id=id).first()
    return jsonify(res.to_json())
