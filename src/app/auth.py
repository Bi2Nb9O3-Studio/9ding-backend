from hashlib import sha256
from functools import wraps
import os
import random
import re
import time
from typing import Tuple
import flask
from app import utils
import app.models.database as database
import json

# salt = "d39d977837414790d42ecd351f59da887d7c41f1a62b5463475bf1c6dc1bd556"
#read salt from `security.cfg`, formation:json key:salt.
with open("./security.cfg", "r", encoding="utf-8") as f:
    salt = json.loads(f.read())["salt"]
def verify_password(username: str, password: str) -> Tuple[bool, str]:
    # get the password of user
    with database.db.connect() as (con, cur):
        # anti sql injection
        if re.search(r'\W', username) is not None:
            return (False, "用户名不合法")
        cur.execute(f"SELECT password FROM users WHERE username='{username}'")
        result = cur.fetchone()
        if result is None:
            return (False, "用户不存在")
        return (result[0] == sha256((salt+password).encode()).hexdigest(), "密码不正确")


def add_user(username: str, password: str):
    with database.db.connect() as (con, cur):
        cur.execute(
            f"INSERT INTO users (username, password) VALUES ('{username}', '{sha256((salt+password).encode()).hexdigest()}')")


def remove_user(uid: str):
    with database.db.connect() as (con, cur):
        cur.execute(f"DELETE FROM users WHERE id='{uid}'")


def change_password(userid: int, password: str):
    with database.db.connect() as (con, cur):
        cur.execute(
            f"UPDATE users SET password='{sha256((salt+password).encode()).hexdigest()}' WHERE id='{userid}'")


def set_logined_status(username, respone: flask.Response):
    respone.set_cookie("username", username, max_age=60 *
                       60*24, expires=60*60*24)
    respone.set_cookie("verification", generate_verification(username), max_age=60*60, expires=60*60)


def set_logout_status(respone: flask.Response):
    respone.delete_cookie("username")
    respone.set_cookie("verification")


def logined_valid(request: flask.Request):
    if request.cookies.get("username") is None or request.cookies.get("verification") is None or request.cookies.get("username") == "" or request.cookies.get("verification") == "":
        return False
    # return request.cookies.get("verification") == sha256((salt+request.cookies.get("username")+salt).encode()).hexdigest()+sha256(salt.encode()).hexdigest()
    return verification(request.cookies.get("username"), request.cookies.get("verification"))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if logined_valid(flask.request):
            return func(*args, **kwargs)
        else:
            return flask.redirect("/admin/login?failed=true&cause=访问此页面需要登录")
    return wrapper


def all_users():
    with database.db.connect() as (con, cur):
        cur.execute("SELECT id,username,password FROM users")
        return cur.fetchall()


def get_userid(username):
    with database.db.connect() as (con, cur):
        cur.execute(f"SELECT id FROM users WHERE username='{username}'")
        return cur.fetchone()[0]


def verification(username, code):
    try:
        decrypted_data = utils.decrypt(code)
        data = json.loads(decrypted_data[:-16])
        return data["username"]==username and time.time()-data["time"]<3600
    except Exception as e:
        return False

def generate_verification(username):
    return utils.encrypt(json.dumps({"username":username,"time":time.time()}) + ''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 16)))


