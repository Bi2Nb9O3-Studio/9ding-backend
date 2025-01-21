import os
import flask
from flask import jsonify, make_response, request, send_file
from io import BytesIO
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