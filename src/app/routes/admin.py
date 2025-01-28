import os
import flask
from flask import jsonify, make_response, request, send_file
from io import BytesIO
import app.models.database as database
import app.auth as auth
import app.models.config as config

blueprint = flask.Blueprint("admin", __name__)

@blueprint.route("/admin/login", methods=["POST"])
def login():
    data = request.get_json()
    if not auth.verify_password(data["username"], data["password"]):
        return jsonify({"error": "login failed"}), 401
    response = jsonify({"success": "login success"})
    auth.set_logined_status(data["username"], response)
    return response


@blueprint.route("/admin/logout", methods=["POST"])
@auth.login_required
def logout():
    response = jsonify({"success": "logout success"})
    auth.set_logout_status(response)
    return response


@blueprint.route("/admin/new_user", methods=["POST"])
@auth.login_required
def add_user():
    data = request.get_json()
    auth.add_user(data["username"], data["password"])
    return jsonify({"success": "add user success"})


@blueprint.route("/admin/rm_user", methods=["POST","DELETE"])
@auth.login_required
def remove_user():
    data = request.get_json()
    auth.remove_user(data["username"])
    return jsonify({"success": "remove user success"})


@blueprint.route("/admin/mod_user", methods=["POST", "PUT"])
@auth.login_required
def change_password():
    data = request.get_json()
    auth.change_password(data["username"], data["password"])
    return jsonify({"success": "change password success"})
