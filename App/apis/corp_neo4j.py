from flask import Blueprint, jsonify
from App.dao.neo4j import get_all_triplets, get_triplets_by_code, get_triplets_by_industry

# （蓝图的名字，导入的名字）
corp_neo4j = Blueprint('corp_neo4j', __name__)


# 获取企业知识图谱中的所有三元组
@corp_neo4j.route('/corp_neo4j/get_all_triplets', methods=['GET'])
def get_all_triplets_():
    relationships = get_all_triplets()
    res = {'status': 200, 'msg': '请求成功', 'data': relationships}
    return jsonify(res)


# 通过企业代码查询相关的三元组
@corp_neo4j.route('/corp_neo4j/get_triplets_by_code/<NSRSBM>/<NSRMC>/<SSXDM>', methods=['GET'])
def _get_triplets_by_code(NSRSBM, NSRMC, SSXDM):
    print(f"request for {NSRSBM}'s triplets")
    relationships = get_triplets_by_code(NSRSBM)
    res = {'status': 200, 'msg': '请求成功', 'data': relationships}
    return jsonify(res)


# 通过行业名称查询相关公司的三元组
@corp_neo4j.route('/corp_neo4j/get_triplets_by_industry/<industry>', methods=['GET'])
def _get_triplets_by_industry(industry):
    print(f"request for {industry}'s triplets")
    relationships = get_triplets_by_industry(industry)
    res = {'status': 200, 'msg': '请求成功', 'data': relationships}
    return jsonify(res)
