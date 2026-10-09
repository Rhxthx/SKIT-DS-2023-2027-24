import os
import uuid

from flask import Blueprint, jsonify, request, current_app

from app.models.prediction import predictions, make_prediction

predictions_bp = Blueprint("predictions", __name__)

# only allow these image types to be uploaded
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def serialize(doc):
    # mongodb gives back an ObjectId and a datetime which are not json
    # serializable, so convert them to strings before sending
    doc["_id"] = str(doc["_id"])
    if doc.get("created_at"):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


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

    # real yolo detections come in the Model Integration sprint. for now we
    # store an empty list so the prediction record still gets saved in the db.
    detections = []

    # user authentication is added later, so no user is linked yet
    doc = make_prediction(user_id=None, image_path=save_path, detections=detections)
    result = predictions().insert_one(doc)
    doc["_id"] = result.inserted_id

    return jsonify(serialize(doc)), 201


@predictions_bp.get("/")
def history():
    # return the saved predictions, newest first
    items = list(predictions().find().sort("created_at", -1).limit(50))
    return jsonify({"predictions": [serialize(d) for d in items]})
