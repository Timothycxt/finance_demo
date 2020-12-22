import json
# encoding='utf8'
from flask import Blueprint, jsonify
from flask_paginate import Pagination
from sqlalchemy import func

from App.models.corp_info import CorpInfo

# （蓝图的名字，导入的名字）
corp_info = Blueprint('corp_info', __name__)


# 展示企业信息列表,每页展示10条
@corp_info.route('/corp_info/<page>/<pre_page>', methods=['GET'])
def corp_list(page,pre_page):
    page=int(page)
    pre_page=int(pre_page)

    total=CorpInfo.query.count()
    start=(page-1)*pre_page
    end=start+pre_page
    pagination=Pagination(bs_version=3,page=page,total=total)
    corp_list=CorpInfo.query.slice(start,end)

    items = []
    data = {}
    res = {}
    for corp in corp_list:
        tmp = corp.to_json()
        time=str(tmp['establish_date'])
        tmp = {
            'id':tmp['id'],
            'code': tmp['code'],
            'name': tmp['name'],
            'type': tmp['type'],
            'legalPerson': tmp['legal_person'],
            'registCapital': tmp['regist_capital'],
            'industry': tmp['industry'],
            'establishDate': time,
            'businessScope': tmp['business_scope'],
            'member': tmp['member']
        }
        items.append(tmp)

    data['items'] = items
    data['total'] = total

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)


# 一家企业信息列表,不用分页
@corp_info.route('/corp_info/<corporation>', methods=['GET'])
def corp_by_name(corporation):
    total =1
    corp_infos = CorpInfo.query.filter(CorpInfo.name==corporation)

    items=[]
    data = {}
    res = {}

    for corp_info in corp_infos:
        tmp = corp_info.to_json()
        time=str(tmp['establish_date'])
        tmp = {
            'id':tmp['id'],
            'code': tmp['code'],
            'name': tmp['name'],
            'type': tmp['type'],
            'legalPerson': tmp['legal_person'],
            'registCapital': tmp['regist_capital'],
            'industry': tmp['industry'],
            'establishDate': time,
            'businessScope': tmp['business_scope'],
            'member': tmp['member']
        }
        items.append(tmp)
    data['items']=items
    data['total']=total

    res['status']=200
    res['msg']='请求成功'
    res['data']=data
    return jsonify(res)


@corp_info.route('/corp/add', methods=['POST'])
def addCorp():
    corpInfo = CorpInfo()
    corpInfo.name = "test"
    corpInfo.save()
    return 'res'