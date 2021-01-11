from flask import Blueprint, jsonify

from App.models import simu_cacu
from App.models.corp_score import Corp_score

corp_score = Blueprint('corp_score', __name__)


@corp_score.route('/corp_score/update_all', methods=['GET'])
def corp_score_update():
    msg = simu_cacu.score_update()
    res = {}
    res['status'] = 200
    res['msg'] = '更新成功'
    res['data'] = msg
    return jsonify(res)
