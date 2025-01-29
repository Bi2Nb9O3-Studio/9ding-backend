import os
import flask
from flask import jsonify, make_response, redirect, request, send_file
from io import BytesIO
import app.models.database as database
import app.auth as auth
import app.models.config as config

blueprint = flask.Blueprint("admin", __name__)

@blueprint.route("/admin/login", methods=["POST"])
def login():
    '''
    登录
    POST /admin/login
    data:{
        "username": "username",
        "password": "password"
    }
    '''
    data = request.form
    valid = auth.verify_password(data["username"], data["password"])
    if not valid[0]:
        return redirect("/admin/login?failed=true&cause="+valid[1])
    response = redirect("/admin/pic")
    auth.set_logined_status(data["username"], response)
    return response


@blueprint.route("/admin/logout", methods=["POST"])
@auth.login_required
def logout():
    '''
    登出
    POST /admin/logout
    `need login`
    '''
    response = jsonify({"success": "logout success"})
    auth.set_logout_status(response)
    return response


@blueprint.route("/admin/new_user", methods=["POST"])
@auth.login_required
def add_user():
    '''
    添加用户
    POST /admin/new_user
    data:{
        "username": "username",
        "password": "password"
    }
    `need login`
    '''
    data = request.get_json()
    auth.add_user(data["username"], data["password"])
    return jsonify({"success": "add user success"})


@blueprint.route("/admin/rm_user", methods=["POST","DELETE"])
@auth.login_required
def remove_user():
    '''
    移除用户
    POST /admin/rm_user
    data:{
        "username": "username"
    }
    `need login`
    '''
    data = request.get_json()
    auth.remove_user(data["username"])
    return jsonify({"success": "remove user success"})


@blueprint.route("/admin/mod_user", methods=["POST", "PUT"])
@auth.login_required
def change_password():
    '''
    POST /admin/mod_user
    data:{
        "username": "username",
        "password": "password"
    }
    need login
    '''
    data = request.get_json()
    auth.change_password(data["username"], data["password"])
    return jsonify({"success": "change password success"})

