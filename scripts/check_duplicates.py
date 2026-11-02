from pathlib import Path
import hashlib
from PIL import Image
import csv

# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

IMAGE_DIR = (
    Path.home()
    / "Downloads"
    / "task_6_final_186_extracted"
    / "task_6_final"
    / "images"
    / "train"
)

REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

EXACT_REPORT = REPORT_DIR / "exact_duplicates.csv"
NEAR_REPORT = REPORT_DIR / "near_duplicates.csv"


# --------------------------------------------------
# Exact duplicate detection using SHA-256
# --------------------------------------------------

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(8192)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def find_exact_duplicates(images):
    hash_groups = {}

    for image in images:
        file_hash = calculate_sha256(image)

        hash_groups.setdefault(file_hash, []).append(image)

    duplicates = []

    for file_hash, files in hash_groups.items():
        if len(files) > 1:
            duplicates.append((file_hash, files))

    return duplicates


# --------------------------------------------------
# Simple perceptual hash
# --------------------------------------------------

def perceptual_hash(image_path, size=16):
    image = Image.open(image_path).convert("L")
    image = image.resize((size, size))

    pixels = list(image.getdata())
    average = sum(pixels) / len(pixels)

    return "".join(
        "1" if pixel >= average else "0"
        for pixel in pixels
    )


def hamming_distance(hash1, hash2):
    return sum(a != b for a, b in zip(hash1, hash2))


def find_near_duplicates(images, threshold=8):
    hashes = {}

    for image in images:
        try:
            hashes[image] = perceptual_hash(image)
        except Exception as e:
            print(f"Could not process {image.name}: {e}")

    pairs = []

    for i in range(len(images)):
        for j in range(i + 1, len(images)):

            image1 = images[i]
            image2 = images[j]

            distance = hamming_distance(
                hashes[image1],
                hashes[image2]
            )

            if distance <= threshold:
                pairs.append(
                    (image1, image2, distance)
                )

    return pairs


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    images = sorted(
        IMAGE_DIR.glob("*.jpg")
    )

    print("=" * 60)
    print("DUPLICATE IMAGE ANALYSIS")
    print("=" * 60)

    print(f"Images checked: {len(images)}")

    # ------------------------------
    # Exact duplicates
    # ------------------------------

    exact_duplicates = find_exact_duplicates(images)

    print()
    print("EXACT DUPLICATES")
    print("-" * 60)

    if exact_duplicates:

        for file_hash, files in exact_duplicates:

            print("\nDuplicate group:")

            for file in files:
                print(f"  {file.name}")

    else:
        print("No exact duplicates found.")

    # Save exact duplicate report

    with open(
        EXACT_REPORT,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "Hash",
                "Duplicate_Files"
            ]
        )

        for file_hash, files in exact_duplicates:

            writer.writerow(
                [
                    file_hash,
                    " | ".join(
                        file.name for file in files
                    )
                ]
            )

    # ------------------------------
    # Near duplicates
    # ------------------------------

    print()
    print("NEAR DUPLICATES")
    print("-" * 60)

    near_duplicates = find_near_duplicates(
        images,
        threshold=8
    )

    if near_duplicates:

        for image1, image2, distance in near_duplicates:

            print(
                f"{image1.name} <-> "
                f"{image2.name} "
                f"(distance={distance})"
            )

    else:

        print("No near duplicates found.")

    # Save near duplicate report

    with open(
        NEAR_REPORT,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "Image_1",
                "Image_2",
                "Hamming_Distance"
            ]
        )

        for image1, image2, distance in near_duplicates:

            writer.writerow(
                [
                    image1.name,
                    image2.name,
                    distance
                ]
            )

    # ------------------------------
    # Final summary
    # ------------------------------

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"Total images checked     : {len(images)}")
    print(
        f"Exact duplicate groups   : "
        f"{len(exact_duplicates)}"
    )
    print(
        f"Near duplicate pairs     : "
        f"{len(near_duplicates)}"
    )

    print()
    print(f"Exact report : {EXACT_REPORT}")
    print(f"Near report  : {NEAR_REPORT}")


if __name__ == "__main__":
    main()