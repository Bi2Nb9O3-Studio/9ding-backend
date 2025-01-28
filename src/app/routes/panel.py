from flask import Blueprint, request, jsonify
import app.models.config as config
import app.auth as auth
from app.routes.admin import login

blueprint = Blueprint("panel", __name__)


@blueprint.route("/panel/config", methods=["POST", "PUT"])
@auth.login_required
def setconfig():
    '''
    设置新的配置
    POST /panel/config
    PUT /panel/config
    data: newdata
    '''
    data = request.get_json()
    config.panelconfig.set(data)
    return jsonify({"message": "success", "status": 200}), 200


@blueprint.route("/panel/config", methods=["GET"])
def getconfig():
    '''
    获取配置
    '''
    return jsonify(config.panelconfig.data), 200
