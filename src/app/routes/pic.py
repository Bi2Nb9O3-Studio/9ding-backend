import os
import flask
from flask import jsonify, request, send_file
from io import BytesIO
import app.models.database as database
import app.utils as utils
import app.models.config as config
import app.auth as auth

blueprint = flask.Blueprint("pic", __name__)


@blueprint.route("/api/content/new", methods=["POST", "PUT"])
@auth.login_required
def post_image():
    '''
    POST /api/content/new
    formation:
    ```{
        "image": "base64",
        "stu_name": "name",
        "category": "category",
        "work_name": "name",
        "teacher": "teacher"
    }```
    '''
    try:
        d = request.get_json()
        # save into database
        with database.db.connect() as (con, cur):
            cur.execute("INSERT INTO images (author, name, category, teacher, image) VALUES (?,?,?,?,?)",
                        (d["stu_name"], d["work_name"], d["category"], d["teacher"], d["image"]))
            con.commit()
        return jsonify({"message": "success", "status": 200, "id": cur.lastrowid}), 200
    except Exception as e:
        return jsonify({"message": "error", "status": 500, "error": str(e)}), 500
# TODO Auth


@blueprint.route("/api/content/<int:id>", methods=["GET"])
def get_image(id):
    with database.db.connect() as (con, cur):
        cur.execute("SELECT * FROM images WHERE id=?", (id,))
        data = cur.fetchone()
    if not data:
        return jsonify({"message": "not found", "status": 404}), 404
    # process data with watermark
    # decode image
    image = utils.imgopen(data[5])
    # add watermark
    txt = utils.watermarktxt(request, id)
    image = utils.watermarkimg(image, txt)
    imageio = BytesIO()
    image.save(imageio, format="PNG")
    imageio.seek(0)
    return send_file(imageio, mimetype="image/png")


@blueprint.route("/api/content/<int:id>", methods=["POST", "PUT"])
@auth.login_required
def modify_image(id):
    d = request.get_json()
    try:
        # if not exist
        with database.db.connect() as (con, cur):
            cur.execute("SELECT * FROM images WHERE id=?", (id,))
            if not cur.fetchone():
                return jsonify({"message": f"image(id={id}) not found,please post first", "status": 404}), 404

        with database.db.connect() as (con, cur):
            cur.execute("UPDATE images SET author=?, name=?, category=?, teacher=?, image=? WHERE id=?",
                        (d["stu_name"], d["work_name"], d["category"], d["teacher"], d["image"], id))
            con.commit()
        return jsonify({"message": "success", "status": 200}), 200
    except Exception as e:
        return jsonify({"message": "error", "status": 500, "error": repr(e)}), 500


@blueprint.route("/api/content/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_image(id):
    with database.db.connect() as (con, cur):
        cur.execute("DELETE FROM images WHERE id=?", (id,))
        con.commit()
    return jsonify({"message": "success", "status": 200}), 200


@blueprint.route("/api/config", methods=["POST", "PUT"])
@auth.login_required
def setconfig():
    data = request.get_json()
    config.picconfig.set(data)
    return jsonify({"message": "success", "status": 200}), 200


@blueprint.route("/api/config", methods=["GET"])
def getconfig():
    return jsonify(config.picconfig.data), 200


@blueprint.route("/api/metadata", methods=["GET"])
def getmetadata():
    '''
    return list,for each:
    {
        "url": "./content/<id>",
        "info": {
            "stu_name": ...,
            "category": ...,
            "work_name": ...,
            "teacher": ...
        }
    }
    '''
    try:
        with database.db.connect() as (con, cur):
            cur.execute("SELECT * FROM images")
            data = cur.fetchall()
        resp = []
        for i in data:
            # 转义

            resp.append({
                "url": f"./content/{i[0]}",
                "info": {
                    "stu_name": i[1],
                    "category": i[3],
                    "work_name": i[2],
                    "teacher": i[4]
                }
            })
        return jsonify(resp), 200
    except Exception as e:
        return jsonify({"message": "error", "status": 500, "error": str(e)}), 500
    # return jsonify(data), 200


@blueprint.route("/api/model.glb", methods=["GET"])
def getmodel():
    return send_file(os.path.abspath("./models/model.glb"), mimetype="model/glb")


@blueprint.route("/api/model.glb", methods=["POST", "PUT"])
@auth.login_required
def setmodel():
    f = request.files["model"]
    f.save(os.path.abspath("./models/model.glb"))
    return jsonify({"message": "success", "status": 200}), 200