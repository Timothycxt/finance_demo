import json
from flask import Blueprint, jsonify
from App.models.corp_info import CorpInfo
from flask_paginate import Pagination,get_page_parameter,request

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

    res={}
    data=[]
    data.append({'total':total})

    for corp in corp_list:
        tmp=corp.to_json()
        tmp={
            '企业代码':tmp['code'],
            '企业名称':tmp['name'],
            '企业类型':tmp['type'],
            '法人代表':tmp['legal_person'],
            '注册资金':tmp['regist_capital'],
            '所在行业':tmp['industry'],
            '创建时间':tmp['establish_date'],
            '经营范围':tmp['business_scope'],
            '主要成员':tmp['member']
        }
        data.append(tmp)

    res['status']=200
    res['msg']='请求成功'
    res['data']=data
    return jsonify(res)


# 一家企业信息列表,不用分页
@corp_info.route('/corp_info/<corporation>', methods=['GET'])
def corp_by_name(corporation):
    total =1
    corp_infos = CorpInfo.query.filter(CorpInfo.name==corporation)
    res = {}
    data = []
    data.append({'total': total})
    for corp_info in corp_infos:
        tmp = corp_info.to_json()
        tmp = {
            '企业代码': tmp['code'],
            '企业名称': tmp['name'],
            '企业类型': tmp['type'],
            '法人代表': tmp['legal_person'],
            '注册资金': tmp['regist_capital'],
            '所在行业': tmp['industry'],
            '创建时间': tmp['establish_date'],
            '经营范围': tmp['business_scope'],
            '主要成员': tmp['member']
        }
        data.append(tmp)

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)


@corp_info.route('/corp/add', methods=['POST'])
def addCorp():
    corpInfo = CorpInfo()
    corpInfo.name = "test"
    corpInfo.save()
    return 'res'