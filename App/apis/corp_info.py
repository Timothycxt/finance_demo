import json
# encoding='utf8'
from flask import Blueprint, jsonify
from App.models.corp_info import CorpInfo

# （蓝图的名字，导入的名字）
corp_info = Blueprint('corp_info', __name__)

<<<<<<< HEAD
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
            'code':tmp['code'],
            'name':tmp['name'],
            'type':tmp['type'],
            'legal_person':tmp['legal_person'],
            'regist_capital':tmp['regist_capital'],
            'industry':tmp['industry'],
            'establish_date':tmp['establish_date'],
            'business_scope':tmp['business_scope'],
            'member':tmp['member']
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
            'code': tmp['code'],
            'name': tmp['name'],
            'type': tmp['type'],
            'legal_person': tmp['legal_person'],
            'regist_capital': tmp['regist_capital'],
            'industry': tmp['industry'],
            'establish_date': tmp['establish_date'],
            'business_scope': tmp['business_scope'],
            'member': tmp['member']
        }
        data.append(tmp)

=======
# 模拟登录接口
@corp_info.route('/corp/login', methods=['POST'])
def login():
    data = {
        'token': 'admin-token'
    }
    res = {}  # 返回一个字典，包含状态码，信息，数据
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)

@corp_info.route('/corp/info', methods=['GET'])
def info():
    data = {
        'roles': '[admin]',
        'name': 'Super Admin',
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
    }
    res = {}  # 返回一个字典，包含状态码，信息，数据
>>>>>>> 54d1c3d4daed5f33455c11d0a78eba97b5c8ab96
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


@corp_info.route('/corp', methods=['GET'])
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


@corp_info.route('/corp/<name>', methods=['GET'])
def corp_by_name(name):
    corp = CorpInfo.query.filter_by(name=name).first()
    res = {}
    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = corp.to_json()
    return jsonify(res)
