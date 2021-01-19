# encoding='utf8'
import functools

from flask import request, jsonify, current_app, Blueprint
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from App.utils.config_helper import get_config_map

authen = Blueprint('authen', __name__)

config_map = get_config_map()


def create_token(api_user=1):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    # 接收用户id转换与编码
    token = s.dumps({"id": api_user}).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        s.loads(token)
    except Exception:
        return None
    return True


def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["z-token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code=4003, msg='缺少参数token')
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code=4004, msg="未授权")
        return view_func(*args, **kwargs)

    return verify_token


@authen.route('/login', methods=['POST'])
def login():
    res_dir = request.get_json()
    if res_dir is None:
        # 这里的code，依然推荐用一个文件管理状态
        return jsonify(code=4002, msg="未接收到参数")
    # 获取前端传过来的参数
    password = res_dir.get("password")
    if password != config_map['app']['password']:
        return jsonify(code=4001, msg="密码验证失败")
    # 获取用户id，传入生成token的方法，并接收返回的token
    token = create_token()
    # 把token返回给前端
    return jsonify(code=2000, msg="成功", data=token)
