import os
import csv
import cv2
import numpy as np

# ============================================================
# TASK 6.3 — POOR QUALITY IMAGE CHECK
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGE_DIR = os.path.join(
    PROJECT_ROOT,
    "dataset",
    "cleaned_final",
    "images",
    "train"
)

REPORT_PATH = os.path.join(
    PROJECT_ROOT,
    "scripts",
    "task_6_3_poor_quality_images_report.csv"
)

# -----------------------------
# Quality thresholds
# -----------------------------

# Images smaller than this will be flagged
MIN_WIDTH = 200
MIN_HEIGHT = 200

# Lower variance of Laplacian = more blurry
BLUR_THRESHOLD = 80.0

# Very dark / very bright thresholds
DARK_THRESHOLD = 40.0
BRIGHT_THRESHOLD = 220.0

# Percentage of extremely dark/bright pixels
EXTREME_PIXEL_PERCENT = 0.85


def check_image(image_path):
    """
    Check one image for:
    1. Very low resolution
    2. Severe blur
    3. Very dark image
    4. Very bright / washed-out image
    """

    problems = []

    image = cv2.imread(image_path)

    # Could not read image
    if image is None:
        problems.append("Unreadable")

        return {
            "status": "POOR_QUALITY",
            "problems": "; ".join(problems),
            "width": "",
            "height": "",
            "blur_score": "",
            "brightness": ""
        }

    height, width = image.shape[:2]

    # --------------------------------
    # 1. Resolution check
    # --------------------------------

    if width < MIN_WIDTH or height < MIN_HEIGHT:
        problems.append("Very low resolution")

    # --------------------------------
    # Convert to grayscale
    # --------------------------------

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # --------------------------------
    # 2. Blur check
    # --------------------------------

    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur_score < BLUR_THRESHOLD:
        problems.append("Severely blurred")

    # --------------------------------
    # 3. Brightness check
    # --------------------------------

    brightness = float(np.mean(gray))

    dark_pixels = np.mean(gray < 40)
    bright_pixels = np.mean(gray > 220)

    if brightness < DARK_THRESHOLD:
        problems.append("Very dark")

    elif dark_pixels >= EXTREME_PIXEL_PERCENT:
        problems.append("Mostly dark")

    if brightness > BRIGHT_THRESHOLD:
        problems.append("Very bright/washed out")

    elif bright_pixels >= EXTREME_PIXEL_PERCENT:
        problems.append("Mostly bright")

    # --------------------------------
    # Final status
    # --------------------------------

    if problems:
        status = "REVIEW_REQUIRED"
    else:
        status = "PASS"

    return {
        "status": status,
        "problems": "; ".join(problems),
        "width": width,
        "height": height,
        "blur_score": round(blur_score, 2),
        "brightness": round(brightness, 2)
    }


# ============================================================
# MAIN
# ============================================================

print()
print("=" * 60)
print("TASK 6.3 — POOR QUALITY IMAGE CHECK")
print("=" * 60)

print(f"Image directory : {IMAGE_DIR}")

if not os.path.exists(IMAGE_DIR):
    print()
    print("ERROR: Image directory not found.")
    print(IMAGE_DIR)
    print()
    input("Press Enter to exit...")
    raise SystemExit


# Supported image formats
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
        for file in os.listdir(IMAGE_DIR)
        if file.lower().endswith(valid_extensions)
    ]
)

print(f"Images found    : {len(images)}")
print()
print("Checking image quality...")
print()

results = []

for index, image_name in enumerate(images, start=1):

    image_path = os.path.join(IMAGE_DIR, image_name)

    result = check_image(image_path)

    results.append({
        "image": image_name,
        **result
    })

    # Progress every 50 images
    if index % 50 == 0 or index == len(images):
        print(f"Checked {index}/{len(images)}")


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
            "status",
            "problems",
            "width",
            "height",
            "blur_score",
            "brightness"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


# ============================================================
# SUMMARY
# ============================================================

total = len(results)

review_required = sum(
    1
    for result in results
    if result["status"] == "REVIEW_REQUIRED"
)

passed = sum(
    1
    for result in results
    if result["status"] == "PASS"
)

print()
print("=" * 60)
print("TASK 6.3 — RESULTS")
print("=" * 60)

print(f"Total images checked : {total}")
print(f"Passed               : {passed}")
print(f"Review required      : {review_required}")

print()
print("Report created:")
print(REPORT_PATH)

print()

if review_required == 0:
    print("RESULT: No poor-quality images automatically detected.")
else:
    print(
        f"RESULT: {review_required} image(s) require manual quality review."
    )

print()
print("IMPORTANT:")
print("No images were deleted or modified.")
print("Task 6.3 only identifies technically poor-quality images.")
print("Irrelevant/no-animal images will be handled in Task 6.4.")

print()
print("TASK 6.3 COMPLETED")
print("=" * 60)
