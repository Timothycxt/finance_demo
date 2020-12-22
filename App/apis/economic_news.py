from flask import Blueprint
from flask import jsonify
from flask_paginate import Pagination

from App.models.economic_news import EconomicNews

economic_new = Blueprint('economic_news', __name__)


@economic_new.route('/economic_news/<page>/<pre_page>', methods=['GET'])
def economic_news(page,pre_page):
    page = int(page)
    pre_page = int(pre_page)

    total = EconomicNews.query.count()
    start = (page - 1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    corp_list = EconomicNews.query.slice(start, end)

    res = {}
    data = []
    data.append({'total': total})

    for corp in corp_list:
        tmp = corp.to_json()
        tmp = {
            'title': tmp['title'],
            'link': tmp['link'],
            'publish_date': tmp['publish_date']
        }
        data.append(tmp)

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)