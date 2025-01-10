import flask
from flask import jsonify, request, send_file
from io import BytesIO
import app.models.database as database
import app.utils as utils
import app.models.config as config

blueprint=flask.Blueprint("pic", __name__)



@blueprint.route("/api/post-image", methods=["POST"])
def post_image():
    # get image from request
    # process image
    # return processed image
    try:
        d = request.get_json()
        {
            "image": "base64",
            "stu_name": "name",
            "category": "category",
            "work_name": "name",
            "teacher": "teacher"
        }
        # save into database
        with database.db.connect() as (con, cur):
            cur.execute("INSERT INTO images (author, name, category, teacher, image) VALUES (?,?,?,?,?)",
                        (d["stu_name"], d["work_name"], d["category"], d["teacher"], d["image"]))
            con.commit()
        return {"message": "success", "status": 200, "id": cur.lastrowid}, 200
    except Exception as e:
        return {"message": "error", "status": 500, "error": str(e)}, 500
# TODO Auth


@blueprint.route("/api/content/<int:id>", methods=["GET"])
def get_image(id):
    with database.db.connect() as (con, cur):
        cur.execute("SELECT * FROM images WHERE id=?", (id,))
        data = cur.fetchone()
    if not data:
        return {"message": "not found", "status": 404}, 404
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


@blueprint.route("/api/config", methods=["POST","PUT"])
def setconfig():
    data=request.get_json()
    config.picconfig.set(data)
    return jsonify({"message":"success","status":200}),200

@blueprint.route("/api/config", methods=["GET"])
def getconfig():
    return jsonify(config.picconfig.data),200