import os
import re
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


@blueprint.route("/admin/logout", methods=["POST",'GET'])
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
    if data['username'].strip() == "" or data['password'].strip() == "":
        return jsonify({"status":400, "reason":"用户名或密码不能未空"}),400
    if re.search(r"\W", data['username']) is not None:
        return jsonify({"status":400, "reason":"用户名不能包含特殊字符"}),400
    all_user = auth.all_users()
    if data['username'] in [i[1] for i in all_user]:
        return jsonify({"status":400, "reason":"用户名已存在"}),400
    auth.add_user(data["username"], data["password"])
    return jsonify({"status":200, "msg":"成功"})


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
    all = auth.all_users()
    # print(type(data['userid']))
    if data['userid'] not in [i[0] for i in all]:
        return jsonify({"status":400, "reason":"用户不存在"}),400
    auth.remove_user(data["userid"])
    if data["userid"] == auth.get_userid(request.cookies.get("username")):
        response = jsonify({"success": "logout success"})
        auth.set_logout_status(response)
        return response
    return jsonify({"status":200,"msg": "remove user success"})


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
    data = request.json
    if re.search(r"\W", data['username']) is not None:
        return jsonify({"status":400, "reason":"用户名不合法"}),400
    with database.db.connect() as (con, cur):
        cur.execute(f"SELECT id FROM users")
        result = cur.fetchall()
        result=[i[0] for i in result]
        if int(data['userid']) not in result:
            return jsonify({"status":"failed", "reason":"用户不存在"})
    auth.change_password(data["userid"], data["newpassword"])
    return jsonify({"status":"success", "msg":"change password success"})


@blueprint.route("/admin/users", methods=["POST"])
@auth.login_required
def users():
    '''
    获取所有用户
    GET /admin/users
    `need login`
    '''
    return jsonify(auth.all_users())

