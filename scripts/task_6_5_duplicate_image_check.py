from pathlib import Path
import hashlib
import csv
from PIL import Image
import imagehash

# ============================================================
# TASK 6.5 — DUPLICATE IMAGE CHECK
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT / "dataset" / "task_6_partial" / "images" / "train"

REPORT_FILE = ROOT / "scripts" / "task_6_5_duplicate_images_report.csv"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

# Near-duplicate threshold
# Smaller value = more strict
PHASH_THRESHOLD = 5


# ============================================================
# CHECK IMAGE DIRECTORY
# ============================================================

print("=" * 60)
print("TASK 6.5 — DUPLICATE IMAGE CHECK")
print("=" * 60)

print()
print("Image directory:")
print(IMAGE_DIR)

if not IMAGE_DIR.exists():
    print()
    print("ERROR: Image directory not found.")
    print(IMAGE_DIR)
    raise SystemExit(1)


# ============================================================
# FIND IMAGES
# ============================================================

images = sorted([
    p for p in IMAGE_DIR.iterdir()
    if p.is_file()
    and p.suffix.lower() in IMAGE_EXTENSIONS
])

print()
print(f"Images found : {len(images)}")


# ============================================================
# EXACT DUPLICATE CHECK
# ============================================================

print()
print("Checking for exact duplicate images...")

hash_map = {}
exact_duplicates = []

for index, image_path in enumerate(images, start=1):

    sha256 = hashlib.sha256()

    try:
        with open(image_path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                sha256.update(chunk)

        file_hash = sha256.hexdigest()

        if file_hash in hash_map:

            original = hash_map[file_hash]

            exact_duplicates.append({
                "image_1": original.name,
                "image_2": image_path.name,
                "type": "EXACT_DUPLICATE",
                "similarity": "100%"
            })

        else:
            hash_map[file_hash] = image_path

    except Exception as e:

        print(
            f"WARNING: Could not process "
            f"{image_path.name}: {e}"
        )

    if index % 25 == 0 or index == len(images):

        print(
            f"Checked {index}/{len(images)}"
        )


# ============================================================
# PERCEPTUAL HASH / NEAR DUPLICATE CHECK
# ============================================================

print()
print("Checking for visually similar images...")

image_hashes = {}

for index, image_path in enumerate(images, start=1):

    try:

        with Image.open(image_path) as img:

            # Convert to RGB so different image formats
            # can be compared consistently
            img = img.convert("RGB")

            image_hashes[image_path] = imagehash.phash(img)

    except Exception as e:

        print(
            f"WARNING: Could not calculate "
            f"perceptual hash for {image_path.name}: {e}"
        )

    if index % 25 == 0 or index == len(images):

        print(
            f"Hashed {index}/{len(images)}"
        )


# ============================================================
# FIND NEAR DUPLICATES
# ============================================================

near_duplicates = []

image_list = list(image_hashes.keys())

for i in range(len(image_list)):

    image_1 = image_list[i]
    hash_1 = image_hashes[image_1]

    for j in range(i + 1, len(image_list)):

        image_2 = image_list[j]
        hash_2 = image_hashes[image_2]

        distance = hash_1 - hash_2

        # Do not report exact duplicates again
        if distance == 0:
            continue

        if distance <= PHASH_THRESHOLD:

            similarity_estimate = max(
                0,
                round(
                    100 -
                    (distance / 64 * 100),
                    2
                )
            )

            near_duplicates.append({
                "image_1": image_1.name,
                "image_2": image_2.name,
                "type": "POSSIBLE_NEAR_DUPLICATE",
                "similarity": f"{similarity_estimate}%"
            })


# ============================================================
# COMBINE RESULTS
# ============================================================

all_duplicates = (
    exact_duplicates +
    near_duplicates
)


# ============================================================
# CREATE REPORT
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
            "image_1",
            "image_2",
            "type",
            "similarity"
        ]
    )

    writer.writeheader()

    for row in all_duplicates:
        writer.writerow(row)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 60)
print("TASK 6.5 — RESULTS")
print("=" * 60)

print()
print(f"Total images checked       : {len(images)}")
print(f"Exact duplicate pairs     : {len(exact_duplicates)}")
print(f"Near-duplicate pairs      : {len(near_duplicates)}")
print(f"Total duplicate candidates: {len(all_duplicates)}")

print()
print("Report created:")
print(REPORT_FILE)

print()
print("IMPORTANT:")
print("- No images were deleted.")
print("- No labels were deleted.")
print("- No annotations were modified.")
print("- Duplicate candidates require review before removal.")

if len(all_duplicates) == 0:

    print()
    print("RESULT: No duplicate candidates detected.")

else:

    print()
    print(
        "RESULT: Duplicate candidates detected."
    )

print()
print("=" * 60)
print("TASK 6.5 DUPLICATE CHECK COMPLETED")
print("=" * 60)