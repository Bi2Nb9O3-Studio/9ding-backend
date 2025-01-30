import os
import flask
from flask import jsonify, make_response, request, send_file
from io import BytesIO
from app import auth
import app.models.database as database
import app.utils as utils
import app.models.config as config
# import app.static

blueprint = flask.Blueprint("static", __name__)

@blueprint.route("/", methods=["GET"])
def index():
    return send_file("static/index.html")

@blueprint.route("/bundle.js", methods=["GET"])
def bundle():
    return send_file("static/bundle.js")


@blueprint.route("/api/content/empty", methods=["GET"])
def empty():
    return send_file("static/empty.png")

@blueprint.route("/admin/login", methods=["GET"])
def login():
    '''
    GET /admin/index
    '''
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
