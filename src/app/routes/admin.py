import json
import os
import re
import flask
from flask import jsonify, make_response, redirect, request, send_file
import app.version as ver
import app.models.database as database
import app.auth as auth
import app.models.config as config
import auto_update as atp

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
    response = redirect("/admin/login")
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

@blueprint.route("/admin/cfghis", methods=["POST"])
@auth.login_required
def cfghis():
    '''
    GET /admin/cfghis
    `need login`
    '''
    with database.db.connect() as (con, cur):
        cur.execute("SELECT * FROM cfg_history")
        result = cur.fetchall()
    return jsonify(result)

@blueprint.route("/admin/revert_config", methods=["POST"])
@auth.login_required
def revert_config():
    '''
    POST /admin/revert_config
    data:{
        "id": "id"
    }
    `need login`
    '''
    map=[
        config.picconfig,
        config.generalconfig,
        config.panelconfig
    ]
    data = request.get_json()
    with database.db.connect() as (con, cur):
        cur.execute(f"SELECT * FROM cfg_history WHERE id={data['id']}")
        result = cur.fetchone()
    map[result[1]].set(json.loads(result[2]))
    return jsonify({"status":200, "msg":"revert success"})

@blueprint.route("/admin/version", methods=["GET"])
@auth.login_required
def version():
    '''
    获取版本号
    GET /admin/version
    `need login`
    '''
    return ver.v

@blueprint.route("/admin/update", methods=["POST"])
@auth.login_required
def update():
    '''
    更新
    POST /admin/update
    `need login`
    '''
    atp.updating = True
    with atp.update_lock:
        atp.updating = True
        q=atp.update_self()
        atp.updating = False
    return jsonify({"status":200, "msg":("success"+(" no new version" if q==1 else "")) if q!=-1 else "无法获取最新版本"})


@blueprint.route("/admin/update/update_bundle", methods=["POST"])
@auth.login_required
def update_bundle():
    '''
    更新bundle
    POST /admin/update_bundle
    `need login`
    '''
    atp.updating = True
    with atp.update_lock:
        atp.updating = True
        q = atp.update_bundle()
        atp.updating = False
    return jsonify({"status": 200, "msg": ("success"+(" no new version" if q == 1 else "")) if q != -1 else "无法获取最新版本"})


@blueprint.route("/admin/update/check_bundle", methods=["POST"])
@auth.login_required
def check_bundle():
    '''
    检查bundle
    POST /admin/check_bundle
    `need login`
    '''
    url, tag = atp.get_latest_release_download_url_tag()
    if atp.checkifnewversion(tag):
        return jsonify({"status":200, "msg":"new version available"})
    return jsonify({"status":200, "msg":"no new version"})


@blueprint.route("/admin/update/check_app", methods=["POST"])
@auth.login_required
def check_app():
    '''
    检查app
    POST /admin/check_app
    `need login`
    '''
    url, tag = atp.get_latest_release_download_url_tag()
    if atp.checkifnewversion(tag, ver.v):
        return jsonify({"status":200, "msg":"new version available"})
    return jsonify({"status":200, "msg":"no new version"})

@blueprint.route("/admin/update/bundle_version", methods=["GET"])
@auth.login_required
def bundle_version():
    '''
    获取bundle版本
    GET /admin/bundle_version
    `need login`
    '''
    with open("./bundle/version", "r") as f:
        version_info = f.read()
    return version_info


@blueprint.route("/admin/update/eta", methods=["GET"])
@auth.login_required
def eta():
    '''
    获取eta
    GET /admin/eta
    `need login`
    '''
    return jsonify({"status":200, "eta":atp.eta})

@blueprint.route("/admin/update/updating", methods=["GET"])
@auth.login_required
def updating():
    '''
    获取更新状态
    GET /admin/updating
    `need login`
    '''
    return jsonify({"status":200, "updating":atp.updating})

@blueprint.route("/admin/update/latest", methods=["GET"])
@auth.login_required
def newer():
    '''
    获取新版本
    GET /admin/latest
    `need login`
    '''
    type=request.args.get("type")
    if type=="app":
        res = atp.get_latest_release_download_url_tag(repo_name="9ding-backend", file_name="app.zip")
        if res=="Failed to retrieve the latest release":
            return jsonify({"status":400, "msg":"Failed to retrieve the latest release"})
        return jsonify({"status":200, "latest":not atp.checkifnewversion(res[1], ver.v)})
    elif type=="bundle":
        res = atp.get_latest_release_download_url_tag()
        if res == "Failed to retrieve the latest release":
            return jsonify({"status": 400, "msg": "Failed to retrieve the latest release"})
        return jsonify({"status": 200, "latest":not atp.checkifnewversion(res[1])})