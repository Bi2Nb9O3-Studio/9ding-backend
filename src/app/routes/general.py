import json
import flask
import app.models.config as config
import app.auth as auth
blueprint = flask.Blueprint("general", __name__)


@blueprint.route("/config.json", methods=["POST", "PUT"])
@auth.login_required
def setconfig():
    '''
    设置新的展馆配置
    POST /config.json
    PUT /config.json
    data: newdata
    '''
    data = flask.request.get_json()
    config.generalconfig.set(data)
    return flask.jsonify({"message": "success", "status": 200}), 200


@blueprint.route("/config.json", methods=["GET"])
def getconfig():
    '''
    获取展馆配置
    GET /config.json
    '''
    resp = json.dumps(config.generalconfig.data)
    return flask.jsonify(json.loads(resp.replace("##SITEURL##", config.panelconfig.data["site-url"]))), 200
