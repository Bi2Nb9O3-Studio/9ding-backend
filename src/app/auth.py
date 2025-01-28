from hashlib import sha256

import flask
import app.models.database as database

salt = "d39d977837414790d42ecd351f59da887d7c41f1a62b5463475bf1c6dc1bd556"

def verify_password(username:str, password:str):
    #get the password of user
    with database.db.connect() as (con, cur):
        cur.execute(f"SELECT password FROM users WHERE username='{username}'")
        result = cur.fetchone()
        if result is None:
            return False
        return result[0] == sha256((salt+password).encode()).hexdigest()


def add_user(username: str, password: str):
    with database.db.connect() as (con, cur):
        cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{sha256((salt+password).encode()).hexdigest()}')")

def remove_user(username: str):
    with database.db.connect() as (con, cur):
        cur.execute(f"DELETE FROM users WHERE username='{username}'")

def change_password(username: str, password: str):
    with database.db.connect() as (con, cur):
        cur.execute(f"UPDATE users SET password='{sha256((salt+password).encode()).hexdigest()}' WHERE username='{username}'")

def set_logined_status(username,respone:flask.Response):
    respone.set_cookie("username",username)
    respone.set_cookie("verification",sha256((salt+username+salt).encode()).hexdigest()+salt)
def set_logout_status(respone:flask.Response):
    respone.set_cookie("username","")
    respone.set_cookie("verification","")
def logined_valid(request:flask.Request):
    return request.cookies.get("verification") == sha256((salt+request.cookies.get("username")+salt).encode()).hexdigest()+salt

def login_required(func):
    def wrapper(*args, **kwargs):
        if logined_valid(flask.request):
            return func(*args, **kwargs)
        else:
            return flask.jsonify({"error": "login required"}), 403
    return wrapper