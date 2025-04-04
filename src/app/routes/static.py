import flask
from flask import jsonify, make_response, redirect, request, send_file
import app.auth as auth
import os


blueprint = flask.Blueprint("static", __name__)

@blueprint.route("/", methods=["GET"])
def index():
    return send_file("static/index.html")

@blueprint.route("/bundle.js", methods=["GET"])
def bundle():
    return send_file("../bundle/bundle.js")


@blueprint.route("/api/content/empty", methods=["GET"])
def empty():
    return send_file("static/empty.png")

@blueprint.route("/admin/login", methods=["GET"])
def login():
    '''
    GET /admin/login
    '''
    if auth.logined_valid(flask.request):
        return redirect("/admin/pic")
    return send_file("static/admin/login.html")

@blueprint.route("/admin/pic", methods=["GET"])
@auth.login_required
def pic():
    '''
    GET /admin/pic
    '''
    return send_file("static/admin/pic.html")


@blueprint.route("/admin/users", methods=["GET"])
@auth.login_required
def users():
    '''
    GET /admin/pic
    '''
    return send_file("static/admin/users.html")

@blueprint.route("/admin/config", methods=["GET"])
@auth.login_required
def config():
    '''
    GET /admin/pic
    '''
    return send_file("static/admin/config.html")

@blueprint.route("/admin/cfghis", methods=["GET"])
@auth.login_required
def cfghis():
    '''
    GET /admin/pic
    '''
    return send_file("static/admin/config_history.html")


@blueprint.route("/admin/about", methods=["GET"])
@auth.login_required
def about():
    '''
    GET /admin/pic
    '''
    return send_file("static/admin/about.html")
