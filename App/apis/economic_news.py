from flask import Blueprint
from flask import jsonify
from flask_paginate import Pagination

from App.apis.authen import login_required
from App.models.economic_news import EconomicNews

economic_new = Blueprint('economic_news', __name__)


@economic_new.route('/economic_news/page/<page>/<pre_page>', methods=['GET'])
@login_required
def economic_news(page, pre_page):
    page = int(page)
    pre_page = int(pre_page)

    total = EconomicNews.query.count()
    start = (page - 1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    corp_list = EconomicNews.query.order_by(EconomicNews.publish_date.desc()).slice(start, end)

    items = []
    res = {}
    data = {}

    for corp in corp_list:
        tmp = corp.to_json()
        time = str(tmp['publish_date'])
        tmp = {
            'id': tmp['id'],
            'title': tmp['title'],
            'link': tmp['link'],
            'publishDate': time
        }
        items.append(tmp)
    data['total'] = total
    data['items'] = items

    res['status'] = 200
    res['msg'] = '请求成功'
    res['data'] = data
    return jsonify(res)
