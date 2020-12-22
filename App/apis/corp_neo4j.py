from flask import Blueprint, jsonify
from App.dao.neo4j import get_all_triplets

# （蓝图的名字，导入的名字）
corp_neo4j = Blueprint('corp_neo4j', __name__)


@corp_neo4j.route('/corp_neo4j/get_all_triplets', methods=['GET'])
def get_all_triplets_():
    relationships = get_all_triplets()
    res = {'status': 200, 'msg': '请求成功', 'data': relationships}
    return jsonify(res)
