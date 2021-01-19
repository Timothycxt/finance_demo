from flask import Blueprint, jsonify

from App.apis.authen import login_required
from App.service import simu_cacu

corp_score = Blueprint('corp_score', __name__)


@corp_score.route('/corp_score/update_all', methods=['GET'])
@login_required
def corp_score_update():
    msg = simu_cacu.score_update()
    res = {}
    res['status'] = 200
    res['msg'] = '更新成功'
    res['data'] = msg
    return jsonify(res)
