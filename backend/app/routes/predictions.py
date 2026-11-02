import os
import uuid

from flask import Blueprint, jsonify, request, current_app

from app.models.prediction import predictions, make_prediction
from app import cloud

predictions_bp = Blueprint("predictions", __name__)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    if doc.get("created_at"):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


def save_image(file):
    # if cloudinary is set up, upload there and return the public url so the
    # image is stored permanently and can be viewed. otherwise save locally.
    if cloud.is_configured():
        return cloud.upload_image(file)

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = uuid.uuid4().hex + "." + ext
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)
    return save_path


@predictions_bp.post("/")
def upload_and_predict():
    if "image" not in request.files:
        return jsonify({"error": "no image file in request"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "no file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "file type not allowed, use jpg or png"}), 400

    image_path = save_image(file)

    detections = []

    doc = make_prediction(user_id=None, image_path=image_path, detections=detections)
    result = predictions().insert_one(doc)
    doc["_id"] = result.inserted_id

    return jsonify(serialize(doc)), 201


@predictions_bp.get("/")
def history():
    items = list(predictions().find().sort("created_at", -1).limit(50))
    return jsonify({"predictions": [serialize(d) for d in items]})
