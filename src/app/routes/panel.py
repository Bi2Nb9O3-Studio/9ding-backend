from flask import Blueprint, request, jsonify
import app.models.config as config

blueprint = Blueprint("panel", __name__)


@blueprint.route("/panel/config", methods=["POST", "PUT"])
def setconfig():
    data = request.get_json()
    config.panelconfig.set(data)
    return jsonify({"message": "success", "status": 200}), 200


@blueprint.route("/panel/config", methods=["GET"])
def getconfig():
    return jsonify(config.panelconfig.data), 200
