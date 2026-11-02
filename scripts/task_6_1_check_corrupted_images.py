from pathlib import Path
from PIL import Image
import csv

# ============================================================
# TASK 6.1 — CORRUPTED IMAGE CHECK
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT / "dataset" / "cleaned_final" / "images" / "train"

REPORT_FILE = ROOT / "scripts" / "task_6_1_corrupted_images_report.csv"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

print("=" * 60)
print("TASK 6.1 — CORRUPTED IMAGE CHECK")
print("=" * 60)

# ------------------------------------------------------------
# CHECK IMAGE DIRECTORY
# ------------------------------------------------------------

if not IMAGE_DIR.exists():
    print("ERROR: Image directory not found:")
    print(IMAGE_DIR)
    raise SystemExit(1)

# ------------------------------------------------------------
# FIND IMAGES
# ------------------------------------------------------------

images = sorted(
    [
        file
        for file in IMAGE_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    ],
    key=lambda x: x.name.lower()
)

print(f"Image directory : {IMAGE_DIR}")
print(f"Images found    : {len(images)}")
print()
print("Checking image integrity...")
print()

# ------------------------------------------------------------
# CHECK EACH IMAGE
# ------------------------------------------------------------

valid_images = 0
corrupted_images = []

for index, image_path in enumerate(images, start=1):

    try:
        with Image.open(image_path) as img:
            img.verify()

        valid_images += 1

    except Exception as error:

        corrupted_images.append({
            "image": image_path.name,
            "status": "CORRUPTED",
            "error": str(error)
        })

    if index % 50 == 0 or index == len(images):
        print(f"Checked {index}/{len(images)} images")

# ------------------------------------------------------------
# CREATE REPORT
# ------------------------------------------------------------

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "image",
            "status",
            "error"
        ]
    )

    writer.writeheader()

    for row in corrupted_images:
        writer.writerow(row)

# ------------------------------------------------------------
# FINAL RESULTS
# ------------------------------------------------------------

print()
print("=" * 60)
print("TASK 6.1 — RESULTS")
print("=" * 60)

print(f"Total images checked : {len(images)}")
print(f"Valid images         : {valid_images}")
print(f"Corrupted images     : {len(corrupted_images)}")

print()
print("Report created:")
print(REPORT_FILE)

if len(corrupted_images) == 0:
    print()
    print("RESULT: No corrupted images detected.")
else:
    print()
    print("RESULT: Corrupted images detected.")
    print("Review the CSV report before removing anything.")

print()
print("=" * 60)
print("TASK 6.1 COMPLETED")
print("=" * 60)
