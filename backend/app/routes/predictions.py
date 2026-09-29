import os
import uuid

from flask import Blueprint, jsonify, request, current_app

predictions_bp = Blueprint("predictions", __name__)

# only allow these image types to be uploaded
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@predictions_bp.post("/")
def upload_and_predict():
    # check a file was actually sent
    if "image" not in request.files:
        return jsonify({"error": "no image file in request"}), 400

    file = request.files["image"]

    # browser sends an empty filename if nothing was selected
    if file.filename == "":
        return jsonify({"error": "no file selected"}), 400

    # check the file type
    if not allowed_file(file.filename):
        return jsonify({"error": "file type not allowed, use jpg or png"}), 400

    # save with a unique name so two uploads don't overwrite each other
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = uuid.uuid4().hex + "." + ext
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    # running the yolo model comes in the Model Integration sprint.
    # for now we just confirm the upload and validation worked.
    return jsonify({
        "message": "image uploaded",
        "image_path": save_path,
        "detections": [],
        "animal_count": 0,
    }), 201


@predictions_bp.get("/")
def history():
    # will return the logged in user's past predictions
    return jsonify({"message": "history not implemented yet"}), 501
