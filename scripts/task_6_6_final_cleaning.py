from pathlib import Path
import csv
import shutil
import yaml

# ============================================================
# TASK 6.6 — FINAL CLEANING & ANNOTATION VERIFICATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# SOURCE DATASET
# Task 6.4 output / Task 6.5 input
# ============================================================

SOURCE_ROOT = ROOT / "dataset" / "task_6_partial"

SOURCE_IMAGES = SOURCE_ROOT / "images" / "train"
SOURCE_LABELS = SOURCE_ROOT / "labels" / "train"

# ============================================================
# TASK 6.5 DUPLICATE REPORT
# ============================================================

DUPLICATE_REPORT = (
    ROOT
    / "scripts"
    / "task_6_5_duplicate_images_report.csv"
)

# ============================================================
# DATASET YAML
# ============================================================

DATA_YAML = ROOT / "data.yaml"

# ============================================================
# FINAL TASK 6 DATASET
# ============================================================

FINAL_ROOT = ROOT / "dataset" / "task_6_final"

FINAL_IMAGES = FINAL_ROOT / "images" / "train"
FINAL_LABELS = FINAL_ROOT / "labels" / "train"

# ============================================================
# TASK 6.6 REPORT
# ============================================================

REPORT_FILE = (
    ROOT
    / "scripts"
    / "task_6_6_final_cleaning_report.csv"
)

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# ============================================================
# HEADER
# ============================================================

print("=" * 65)
print("TASK 6.6 — FINAL CLEANING & ANNOTATION VERIFICATION")
print("=" * 65)


# ============================================================
# CHECK SOURCE DATASET
# ============================================================

if not SOURCE_IMAGES.exists():

    print()
    print("ERROR: Source image directory not found:")
    print(SOURCE_IMAGES)
    raise SystemExit(1)


if not SOURCE_LABELS.exists():

    print()
    print("ERROR: Source label directory not found:")
    print(SOURCE_LABELS)
    raise SystemExit(1)


if not DUPLICATE_REPORT.exists():

    print()
    print("ERROR: Task 6.5 duplicate report not found:")
    print(DUPLICATE_REPORT)
    raise SystemExit(1)


if not DATA_YAML.exists():

    print()
    print("ERROR: data.yaml not found:")
    print(DATA_YAML)
    raise SystemExit(1)


# ============================================================
# READ DATASET CLASSES
# ============================================================

with open(
    DATA_YAML,
    "r",
    encoding="utf-8"
) as f:

    data = yaml.safe_load(f)


names = data.get("names", [])

class_count = len(names)

print()
print(f"Dataset classes : {class_count}")


# ============================================================
# FIND SOURCE IMAGES
# ============================================================

source_images = sorted([
    p
    for p in SOURCE_IMAGES.iterdir()
    if p.is_file()
    and p.suffix.lower() in IMAGE_EXTENSIONS
])

print()
print(f"Source images : {len(source_images)}")


# ============================================================
# READ TASK 6.5 DUPLICATE REPORT
# ============================================================

duplicate_rows = []

with open(
    DUPLICATE_REPORT,
    "r",
    encoding="utf-8",
    newline=""
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        duplicate_rows.append(row)


print()
print(
    "Duplicate candidates from Task 6.5 : "
    f"{len(duplicate_rows)}"
)


# ============================================================
# SELECT IMAGES FOR AUTOMATIC REMOVAL
#
# RULE:
# For each near-duplicate pair, image_2 is removed.
#
# The original dataset remains untouched.
# ============================================================

images_to_remove = set()

for row in duplicate_rows:

    image_2 = row.get("image_2", "").strip()

    if image_2:

        images_to_remove.add(image_2)


print()
print(
    "Images selected for duplicate removal : "
    f"{len(images_to_remove)}"
)


# ============================================================
# REMOVE PREVIOUS TASK 6 FINAL OUTPUT
# ============================================================

if FINAL_ROOT.exists():

    print()
    print("Previous Task 6 final dataset found.")
    print("Removing previous output so it can be recreated...")

    shutil.rmtree(FINAL_ROOT)


# ============================================================
# CREATE FINAL DATASET DIRECTORIES
# ============================================================

FINAL_IMAGES.mkdir(
    parents=True,
    exist_ok=True
)

FINAL_LABELS.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# COPY RETAINED IMAGES AND LABELS
# ============================================================

copied_images = 0
copied_labels = 0
missing_labels = 0
removed_images = 0

removal_report = []

print()
print("Creating Task 6 final cleaned dataset...")
print()


for image_path in source_images:

    image_name = image_path.name

    # --------------------------------------------------------
    # REMOVE DUPLICATE CANDIDATE
    # --------------------------------------------------------

    if image_name in images_to_remove:

        removed_images += 1

        removal_report.append({
            "image": image_name,
            "status": "REMOVED",
            "reason": "POSSIBLE_NEAR_DUPLICATE"
        })

        continue


    # --------------------------------------------------------
    # COPY RETAINED IMAGE
    # --------------------------------------------------------

    destination_image = FINAL_IMAGES / image_name

    shutil.copy2(
        image_path,
        destination_image
    )

    copied_images += 1


    # --------------------------------------------------------
    # FIND MATCHING LABEL
    # --------------------------------------------------------

    label_path = SOURCE_LABELS / (
        image_path.stem + ".txt"
    )


    if label_path.exists():

        destination_label = FINAL_LABELS / (
            image_path.stem + ".txt"
        )

        shutil.copy2(
            label_path,
            destination_label
        )

        copied_labels += 1


    else:

        missing_labels += 1

        removal_report.append({
            "image": image_name,
            "status": "RETAINED_BUT_MISSING_LABEL",
            "reason": "MISSING_LABEL"
        })


    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    if (
        copied_images % 25 == 0
        or copied_images == len(source_images)
    ):

        print(
            f"Processed {copied_images}/{len(source_images)}"
        )


# ============================================================
# ANNOTATION VALIDATION
# ============================================================

print()
print("Validating final annotations...")


invalid_class_ids = 0
invalid_boxes = 0
malformed_lines = 0
empty_labels = 0
orphan_labels = 0


# ============================================================
# CHECK EVERY FINAL IMAGE
# ============================================================

for image_path in FINAL_IMAGES.iterdir():

    if not image_path.is_file():
        continue

    if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
        continue


    label_path = FINAL_LABELS / (
        image_path.stem + ".txt"
    )


    # --------------------------------------------------------
    # MISSING LABEL
    # --------------------------------------------------------

    if not label_path.exists():

        missing_labels += 1
        continue


    # --------------------------------------------------------
    # READ LABEL
    # --------------------------------------------------------

    with open(
        label_path,
        "r",
        encoding="utf-8"
    ) as f:

        lines = [
            line.strip()
            for line in f
            if line.strip()
        ]


    # --------------------------------------------------------
    # EMPTY LABEL
    # --------------------------------------------------------

    if len(lines) == 0:

        empty_labels += 1
        continue


    # --------------------------------------------------------
    # VALIDATE EACH ANNOTATION
    # --------------------------------------------------------

    for line in lines:

        parts = line.split()


        # YOLO format must contain 5 values
        #
        # class_id
        # x_center
        # y_center
        # width
        # height
        # ---------------------------------------------------

        if len(parts) != 5:

            malformed_lines += 1
            continue


        try:

            class_id = int(parts[0])

            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])


        except ValueError:

            malformed_lines += 1
            continue


        # ----------------------------------------------------
        # CLASS ID VALIDATION
        # ----------------------------------------------------

        if (
            class_id < 0
            or class_id >= class_count
        ):

            invalid_class_ids += 1


        # ----------------------------------------------------
        # BOUNDING BOX VALIDATION
        # ----------------------------------------------------

        if not (
            0 <= x_center <= 1
            and
            0 <= y_center <= 1
            and
            0 < width <= 1
            and
            0 < height <= 1
        ):

            invalid_boxes += 1


# ============================================================
# CHECK ORPHAN LABELS
# ============================================================

final_image_stems = {
    p.stem
    for p in FINAL_IMAGES.iterdir()
    if p.is_file()
    and p.suffix.lower() in IMAGE_EXTENSIONS
}


for label_path in FINAL_LABELS.glob("*.txt"):

    if label_path.stem not in final_image_stems:

        orphan_labels += 1


# ============================================================
# CREATE TASK 6.6 REPORT
# ============================================================

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "image",
            "status",
            "reason"
        ]
    )

    writer.writeheader()


    for row in removal_report:

        writer.writerow(row)


# ============================================================
# FINAL COUNTS
# ============================================================

final_image_count = len([
    p
    for p in FINAL_IMAGES.iterdir()
    if p.is_file()
    and p.suffix.lower() in IMAGE_EXTENSIONS
])


final_label_count = len(
    list(FINAL_LABELS.glob("*.txt"))
)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 65)
print("TASK 6.6 — RESULTS")
print("=" * 65)

print()

print(
    f"Starting images             : "
    f"{len(source_images)}"
)

print(
    f"Duplicate candidates       : "
    f"{len(duplicate_rows)}"
)

print(
    f"Images removed             : "
    f"{removed_images}"
)

print(
    f"Final images               : "
    f"{final_image_count}"
)

print(
    f"Final labels               : "
    f"{final_label_count}"
)


# ============================================================
# ANNOTATION RESULTS
# ============================================================

print()
print("ANNOTATION VALIDATION")
print("---------------------")

print(
    f"Missing labels             : "
    f"{missing_labels}"
)

print(
    f"Orphan labels              : "
    f"{orphan_labels}"
)

print(
    f"Empty labels               : "
    f"{empty_labels}"
)

print(
    f"Invalid class IDs          : "
    f"{invalid_class_ids}"
)

print(
    f"Invalid bounding boxes     : "
    f"{invalid_boxes}"
)

print(
    f"Malformed annotation lines : "
    f"{malformed_lines}"
)


# ============================================================
# PATHS
# ============================================================

print()
print("FINAL TASK 6 DATASET:")
print(FINAL_ROOT)

print()
print("FINAL IMAGES:")
print(FINAL_IMAGES)

print()
print("FINAL LABELS:")
print(FINAL_LABELS)

print()
print("TASK 6.6 REPORT:")
print(REPORT_FILE)


# ============================================================
# IMPORTANT
# ============================================================

print()
print("IMPORTANT:")
print("Original Task 6 partial dataset was NOT modified:")
print(SOURCE_ROOT)


# ============================================================
# COMPLETION
# ============================================================

print()
print("=" * 65)
print("TASK 6.6 COMPLETED")
print("=" * 65)