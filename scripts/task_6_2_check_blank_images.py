from pathlib import Path
from PIL import Image, ImageStat
import csv

# ============================================================
# TASK 6.2 — BLANK IMAGE CHECK
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT / "dataset" / "cleaned_final" / "images" / "train"

REPORT_FILE = ROOT / "scripts" / "task_6_2_blank_images_report.csv"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

# Thresholds for identifying visually blank images
MEAN_THRESHOLD = 5.0
STDDEV_THRESHOLD = 3.0

print("=" * 60)
print("TASK 6.2 — BLANK IMAGE CHECK")
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
print("Checking for blank or near-blank images...")
print()

# ------------------------------------------------------------
# CHECK EACH IMAGE
# ------------------------------------------------------------

blank_images = []
valid_images = 0

for index, image_path in enumerate(images, start=1):

    try:

        with Image.open(image_path) as img:

            # Convert to grayscale
            gray = img.convert("L")

            # Calculate average brightness
            stat = ImageStat.Stat(gray)

            mean_value = stat.mean[0]
            stddev_value = stat.stddev[0]

            # A blank image has extremely little
            # variation in pixel values.
            is_blank = (
                mean_value <= MEAN_THRESHOLD
                or stddev_value <= STDDEV_THRESHOLD
            )

            if is_blank:

                blank_images.append({
                    "image": image_path.name,
                    "status": "BLANK_OR_NEAR_BLANK",
                    "mean_pixel_value": round(mean_value, 2),
                    "pixel_stddev": round(stddev_value, 2)
                })

            else:

                valid_images += 1

    except Exception as error:

        # Corrupted files were already checked in Task 6.1.
        # Record unexpected errors here without deleting anything.
        blank_images.append({
            "image": image_path.name,
            "status": "CHECK_ERROR",
            "mean_pixel_value": "",
            "pixel_stddev": str(error)
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
            "mean_pixel_value",
            "pixel_stddev"
        ]
    )

    writer.writeheader()

    for row in blank_images:
        writer.writerow(row)

# ------------------------------------------------------------
# FINAL RESULTS
# ------------------------------------------------------------

print()
print("=" * 60)
print("TASK 6.2 — RESULTS")
print("=" * 60)

print(f"Total images checked : {len(images)}")
print(f"Non-blank images     : {valid_images}")
print(f"Blank/near-blank     : {len(blank_images)}")

print()
print("Report created:")
print(REPORT_FILE)

if len(blank_images) == 0:

    print()
    print("RESULT: No blank or near-blank images detected.")

else:

    print()
    print("RESULT: Blank/near-blank images detected.")
    print("Review the CSV before removing anything.")

print()
print("=" * 60)
print("TASK 6.2 COMPLETED")
print("=" * 60)
