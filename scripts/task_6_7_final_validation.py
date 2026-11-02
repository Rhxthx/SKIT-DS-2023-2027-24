from pathlib import Path
import csv
import yaml

# ============================================================
# TASK 6.7 — FINAL TASK 6 VALIDATION & REPORT
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

FINAL_ROOT = ROOT / "dataset" / "task_6_final"

IMAGE_DIR = FINAL_ROOT / "images" / "train"
LABEL_DIR = FINAL_ROOT / "labels" / "train"

DATA_YAML = ROOT / "data.yaml"

REPORT_FILE = (
    ROOT
    / "scripts"
    / "task_6_7_final_validation_report.csv"
)

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

print("=" * 65)
print("TASK 6.7 — FINAL TASK 6 VALIDATION & REPORT")
print("=" * 65)

# ============================================================
# CHECK PATHS
# ============================================================

if not IMAGE_DIR.exists():
    print()
    print("ERROR: Final image directory not found:")
    print(IMAGE_DIR)
    raise SystemExit(1)

if not LABEL_DIR.exists():
    print()
    print("ERROR: Final label directory not found:")
    print(LABEL_DIR)
    raise SystemExit(1)

if not DATA_YAML.exists():
    print()
    print("ERROR: data.yaml not found:")
    print(DATA_YAML)
    raise SystemExit(1)

# ============================================================
# LOAD CLASS INFORMATION
# ============================================================

with open(
    DATA_YAML,
    "r",
    encoding="utf-8"
) as f:
    data = yaml.safe_load(f)

names = data.get("names", [])
class_count = len(names)

# ============================================================
# FIND FINAL IMAGES
# ============================================================

images = sorted([
    p
    for p in IMAGE_DIR.iterdir()
    if p.is_file()
    and p.suffix.lower() in IMAGE_EXTENSIONS
])

labels = sorted([
    p
    for p in LABEL_DIR.iterdir()
    if p.is_file()
    and p.suffix.lower() == ".txt"
])

print()
print("FINAL DATASET")
print("-------------")
print(f"Final image directory : {IMAGE_DIR}")
print(f"Final label directory : {LABEL_DIR}")
print(f"Images found          : {len(images)}")
print(f"Labels found          : {len(labels)}")
print(f"Classes in data.yaml  : {class_count}")

# ============================================================
# IMAGE ↔ LABEL MATCHING
# ============================================================

image_stems = {
    p.stem
    for p in images
}

label_stems = {
    p.stem
    for p in labels
}

missing_labels = sorted(
    image_stems - label_stems
)

orphan_labels = sorted(
    label_stems - image_stems
)

# ============================================================
# ANNOTATION VALIDATION
# ============================================================

empty_labels = []
malformed_lines = []
invalid_class_ids = []
invalid_boxes = []

total_objects = 0

for label_path in labels:

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

    # Empty label
    if len(lines) == 0:

        empty_labels.append(label_path.name)
        continue

    for line_number, line in enumerate(
        lines,
        start=1
    ):

        parts = line.split()

        # ----------------------------------------------------
        # YOLO FORMAT CHECK
        # ----------------------------------------------------

        if len(parts) != 5:

            malformed_lines.append(
                f"{label_path.name}:line {line_number}"
            )

            continue

        try:

            class_id = int(parts[0])

            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])

        except ValueError:

            malformed_lines.append(
                f"{label_path.name}:line {line_number}"
            )

            continue

        total_objects += 1

        # ----------------------------------------------------
        # CLASS ID CHECK
        # ----------------------------------------------------

        if (
            class_id < 0
            or class_id >= class_count
        ):

            invalid_class_ids.append(
                f"{label_path.name}:line {line_number}"
            )

        # ----------------------------------------------------
        # BOUNDING BOX CHECK
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

            invalid_boxes.append(
                f"{label_path.name}:line {line_number}"
            )

# ============================================================
# FINAL STATUS
# ============================================================

validation_passed = (
    len(images) > 0
    and
    len(labels) > 0
    and
    len(missing_labels) == 0
    and
    len(orphan_labels) == 0
    and
    len(empty_labels) == 0
    and
    len(malformed_lines) == 0
    and
    len(invalid_class_ids) == 0
    and
    len(invalid_boxes) == 0
)

# ============================================================
# CREATE REPORT
# ============================================================

report_rows = [
    ("final_images", len(images)),
    ("final_labels", len(labels)),
    ("classes", class_count),
    ("total_objects", total_objects),
    ("missing_labels", len(missing_labels)),
    ("orphan_labels", len(orphan_labels)),
    ("empty_labels", len(empty_labels)),
    ("malformed_annotation_lines", len(malformed_lines)),
    ("invalid_class_ids", len(invalid_class_ids)),
    ("invalid_bounding_boxes", len(invalid_boxes)),
    (
        "validation_status",
        "PASSED" if validation_passed else "FAILED"
    )
]

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "metric",
        "value"
    ])

    writer.writerows(report_rows)

# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 65)
print("TASK 6.7 — RESULTS")
print("=" * 65)

print()
print(f"Final images              : {len(images)}")
print(f"Final labels              : {len(labels)}")
print(f"Total annotated objects   : {total_objects}")
print(f"Classes                   : {class_count}")

print()
print("IMAGE ↔ LABEL CHECK")
print("-------------------")
print(f"Missing labels            : {len(missing_labels)}")
print(f"Orphan labels             : {len(orphan_labels)}")

print()
print("ANNOTATION CHECK")
print("----------------")
print(f"Empty labels              : {len(empty_labels)}")
print(f"Malformed lines           : {len(malformed_lines)}")
print(f"Invalid class IDs         : {len(invalid_class_ids)}")
print(f"Invalid bounding boxes    : {len(invalid_boxes)}")

print()
print("FINAL VALIDATION STATUS:")
print(
    "PASSED"
    if validation_passed
    else
    "FAILED"
)

print()
print("Final Task 6 dataset:")
print(FINAL_ROOT)

print()
print("Validation report:")
print(REPORT_FILE)

print()
print("=" * 65)
print("TASK 6.7 COMPLETED")
print("=" * 65)