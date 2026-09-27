import os
import csv
import shutil
from ultralytics import YOLO

# ============================================================
# TASK 6.4 — IRRELEVANT IMAGE CHECK & FINAL CLEANING
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# ------------------------------------------------------------
# SOURCE DATASET
# ------------------------------------------------------------

SOURCE_IMAGE_DIR = os.path.join(
    PROJECT_ROOT,
    "dataset",
    "cleaned_final",
    "images",
    "train"
)

SOURCE_LABEL_DIR = os.path.join(
    PROJECT_ROOT,
    "dataset",
    "cleaned_final",
    "labels",
    "train"
)

# ------------------------------------------------------------
# TASK 6.3 REPORT
# ------------------------------------------------------------

QUALITY_REPORT = os.path.join(
    PROJECT_ROOT,
    "scripts",
    "task_6_3_poor_quality_images_report.csv"
)

# ------------------------------------------------------------
# TASK 6.4 REPORT
# ------------------------------------------------------------

REPORT_PATH = os.path.join(
    PROJECT_ROOT,
    "scripts",
    "task_6_4_irrelevant_images_report.csv"
)

# ------------------------------------------------------------
# FINAL DATASET
# ------------------------------------------------------------

FINAL_DATASET_DIR = os.path.join(
    PROJECT_ROOT,
    "dataset",
    "task_6_final"
)

FINAL_IMAGE_DIR = os.path.join(
    FINAL_DATASET_DIR,
    "images",
    "train"
)

FINAL_LABEL_DIR = os.path.join(
    FINAL_DATASET_DIR,
    "labels",
    "train"
)

# ------------------------------------------------------------
# YOLO MODEL
# ------------------------------------------------------------

MODEL_NAME = "yolov8n.pt"

# Minimum confidence for animal detection
CONFIDENCE_THRESHOLD = 0.20


# ============================================================
# COCO ANIMAL CLASSES
# ============================================================

ANIMAL_CLASSES = {
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe"
}


# ============================================================
# FUNCTIONS
# ============================================================

def load_poor_quality_images():

    poor_quality = set()

    if not os.path.exists(QUALITY_REPORT):
        print()
        print("WARNING: Task 6.3 report was not found.")
        print("The 26 poor-quality images cannot be included automatically.")
        print()

        return poor_quality

    with open(
        QUALITY_REPORT,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["status"] == "REVIEW_REQUIRED":
                poor_quality.add(row["image"])

    return poor_quality


def detect_animals(model, image_path):

    results = model.predict(
        source=image_path,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False
    )

    detected_animals = []

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            if class_name in ANIMAL_CLASSES:

                detected_animals.append(
                    f"{class_name} ({confidence:.2f})"
                )

    return detected_animals


# ============================================================
# MAIN
# ============================================================

print()
print("=" * 65)
print("TASK 6.4 — IRRELEVANT IMAGE CHECK & FINAL CLEANING")
print("=" * 65)

print()
print("Source dataset:")
print(SOURCE_IMAGE_DIR)

print()
print("IMPORTANT:")
print("- Task 6.3 poor-quality images will also be removed.")
print("- Images without a detected genuine animal will be removed.")
print("- Plants / empty scenes / unrelated images will be removed.")
print("- Original cleaned_final dataset will NOT be modified.")
print()


# ============================================================
# CHECK SOURCE DIRECTORY
# ============================================================

if not os.path.exists(SOURCE_IMAGE_DIR):

    print("ERROR: Source image directory not found.")
    print(SOURCE_IMAGE_DIR)
    raise SystemExit


# ============================================================
# GET IMAGES
# ============================================================

valid_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

images = sorted(
    [
        file
        for file in os.listdir(SOURCE_IMAGE_DIR)
        if file.lower().endswith(valid_extensions)
    ]
)

print(f"Images found: {len(images)}")
print()


# ============================================================
# LOAD 6.3 POOR QUALITY RESULTS
# ============================================================

poor_quality_images = load_poor_quality_images()

print(
    f"Poor-quality images from Task 6.3: "
    f"{len(poor_quality_images)}"
)

print()


# ============================================================
# LOAD YOLO
# ============================================================

print("Loading YOLO model...")

model = YOLO(MODEL_NAME)

print("YOLO model loaded.")
print()
print("Checking images for genuine animals...")
print()


# ============================================================
# PROCESS IMAGES
# ============================================================

results = []

kept_images = []
removed_images = []

for index, image_name in enumerate(images, start=1):

    image_path = os.path.join(
        SOURCE_IMAGE_DIR,
        image_name
    )

    # --------------------------------------------------------
    # FIRST: REMOVE 6.3 POOR QUALITY IMAGES
    # --------------------------------------------------------

    if image_name in poor_quality_images:

        results.append({
            "image": image_name,
            "decision": "REMOVE",
            "reason": "Poor quality — Task 6.3",
            "detected_animals": ""
        })

        removed_images.append(image_name)

    else:

        # ----------------------------------------------------
        # DETECT ANIMALS
        # ----------------------------------------------------

        detected_animals = detect_animals(
            model,
            image_path
        )

        # ----------------------------------------------------
        # NO ANIMAL
        # ----------------------------------------------------

        if len(detected_animals) == 0:

            results.append({
                "image": image_name,
                "decision": "REMOVE",
                "reason": "No genuine animal detected",
                "detected_animals": ""
            })

            removed_images.append(image_name)

        # ----------------------------------------------------
        # ANIMAL FOUND
        # ----------------------------------------------------

        else:

            animal_text = "; ".join(
                detected_animals
            )

            results.append({
                "image": image_name,
                "decision": "KEEP",
                "reason": "Genuine animal detected",
                "detected_animals": animal_text
            })

            kept_images.append(image_name)

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    if index % 25 == 0 or index == len(images):

        print(
            f"Checked {index}/{len(images)}"
        )


# ============================================================
# CREATE FRESH FINAL DATASET
# ============================================================

print()
print("=" * 65)
print("CREATING TASK 6 FINAL DATASET")
print("=" * 65)

# Remove old Task 6 final dataset if it exists
if os.path.exists(FINAL_DATASET_DIR):

    print()
    print("Removing previous Task 6 final dataset...")

    shutil.rmtree(FINAL_DATASET_DIR)


os.makedirs(FINAL_IMAGE_DIR, exist_ok=True)
os.makedirs(FINAL_LABEL_DIR, exist_ok=True)


# ============================================================
# COPY RETAINED IMAGES + LABELS
# ============================================================

missing_labels = 0
copied_images = 0
copied_labels = 0

print()
print("Copying retained images and labels...")
print()

for index, image_name in enumerate(
    kept_images,
    start=1
):

    source_image = os.path.join(
        SOURCE_IMAGE_DIR,
        image_name
    )

    destination_image = os.path.join(
        FINAL_IMAGE_DIR,
        image_name
    )

    shutil.copy2(
        source_image,
        destination_image
    )

    copied_images += 1

    # --------------------------------------------------------
    # MATCHING LABEL
    # --------------------------------------------------------

    base_name = os.path.splitext(image_name)[0]

    label_name = base_name + ".txt"

    source_label = os.path.join(
        SOURCE_LABEL_DIR,
        label_name
    )

    destination_label = os.path.join(
        FINAL_LABEL_DIR,
        label_name
    )

    if os.path.exists(source_label):

        shutil.copy2(
            source_label,
            destination_label
        )

        copied_labels += 1

    else:

        missing_labels += 1

    if index % 25 == 0 or index == len(kept_images):

        print(
            f"Copied {index}/{len(kept_images)}"
        )


# ============================================================
# SAVE REPORT
# ============================================================

with open(
    REPORT_PATH,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "image",
            "decision",
            "reason",
            "detected_animals"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


# ============================================================
# SUMMARY
# ============================================================

total = len(images)

removed = len(removed_images)

kept = len(kept_images)

print()
print("=" * 65)
print("TASK 6.4 — RESULTS")
print("=" * 65)

print()
print(f"Starting images       : {total}")
print(f"Images retained       : {kept}")
print(f"Images removed        : {removed}")
print(f"Images copied         : {copied_images}")
print(f"Labels copied         : {copied_labels}")
print(f"Missing labels        : {missing_labels}")

print()
print("Final dataset:")
print(FINAL_DATASET_DIR)

print()
print("Cleaning report:")
print(REPORT_PATH)

print()
print("=" * 65)
print("REMOVAL SUMMARY")
print("=" * 65)

poor_removed = sum(
    1
    for result in results
    if "Poor quality" in result["reason"]
)

no_animal_removed = sum(
    1
    for result in results
    if result["reason"] == "No genuine animal detected"
)

print(
    f"Poor-quality images removed : {poor_removed}"
)

print(
    f"No-animal/irrelevant removed: {no_animal_removed}"
)

print(
    f"Total removed              : {removed}"
)

print()
print("IMPORTANT:")
print("The original dataset was NOT modified:")
print(
    "dataset\\cleaned_final"
)

print()
print("Task 6.4 final cleaned dataset:")
print(
    "dataset\\task_6_final"
)

print()
print("TASK 6.4 COMPLETED")
print("=" * 65)
