import json
import flask
import app.models.config as config
blueprint = flask.Blueprint("general", __name__)


@blueprint.route("/config.json", methods=["POST", "PUT"])
def setconfig():
    data = flask.request.get_json()
    config.generalconfig.set(data)
    return flask.jsonify({"message": "success", "status": 200}), 200


@blueprint.route("/config.json", methods=["GET"])
def getconfig():
    resp = json.dumps(config.generalconfig.data)
    return flask.jsonify(json.loads(resp.replace("##SITEURL##", config.panelconfig.data["site-url"]))), 200
