from pathlib import Path

# ---------------------------------------------------------
# Post-Cleaning Image-Label Quality Check
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIRS = {
    "train": ROOT / "dataset" / "cleaned" / "images" / "train",
    "val": ROOT / "dataset" / "cleaned" / "images" / "val",
}

LABEL_DIRS = {
    "train": ROOT / "dataset" / "cleaned" / "labels" / "train",
    "val": ROOT / "dataset" / "cleaned" / "labels" / "val",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

NUM_CLASSES = 40


def check_split(split):
    image_dir = IMAGE_DIRS[split]
    label_dir = LABEL_DIRS[split]

    images = {
        file.stem
        for file in image_dir.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    }

    labels = {
        file.stem
        for file in label_dir.glob("*.txt")
        if file.is_file()
    }

    images_without_labels = sorted(images - labels)
    labels_without_images = sorted(labels - images)

    empty_labels = []
    malformed_labels = []
    invalid_class_ids = []
    invalid_boxes = []

    for label_file in label_dir.glob("*.txt"):
        if label_file.stat().st_size == 0:
            empty_labels.append(label_file.name)
            continue

        with open(label_file, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                parts = line.strip().split()

                if len(parts) != 5:
                    malformed_labels.append(
                        f"{label_file.name}: line {line_number}"
                    )
                    continue

                try:
                    class_id = int(parts[0])
                    box = [float(value) for value in parts[1:]]
                except ValueError:
                    malformed_labels.append(
                        f"{label_file.name}: line {line_number}"
                    )
                    continue

                if class_id < 0 or class_id >= NUM_CLASSES:
                    invalid_class_ids.append(
                        f"{label_file.name}: line {line_number}"
                    )

                if any(value < 0 or value > 1 for value in box):
                    invalid_boxes.append(
                        f"{label_file.name}: line {line_number}"
                    )

    return {
        "images": len(images),
        "labels": len(labels),
        "images_without_labels": images_without_labels,
        "labels_without_images": labels_without_images,
        "empty_labels": empty_labels,
        "malformed_labels": malformed_labels,
        "invalid_class_ids": invalid_class_ids,
        "invalid_boxes": invalid_boxes,
    }


def print_report(split, result):
    print(f"\n{'=' * 65}")
    print(f"                 {split.upper()} DATASET")
    print(f"{'=' * 65}")

    print(f"Images                  : {result['images']}")
    print(f"Labels                  : {result['labels']}")
    print(f"Images without labels   : {len(result['images_without_labels'])}")
    print(f"Labels without images   : {len(result['labels_without_images'])}")
    print(f"Empty label files       : {len(result['empty_labels'])}")
    print(f"Malformed annotations   : {len(result['malformed_labels'])}")
    print(f"Invalid class IDs       : {len(result['invalid_class_ids'])}")
    print(f"Invalid bounding boxes  : {len(result['invalid_boxes'])}")


def main():
    print("\n" + "=" * 65)
    print("       POST-CLEANING IMAGE-LABEL QUALITY CHECK")
    print("=" * 65)

    all_passed = True

    for split in ["train", "val"]:
        result = check_split(split)
        print_report(split, result)

        if any([
            result["images_without_labels"],
            result["labels_without_images"],
            result["empty_labels"],
            result["malformed_labels"],
            result["invalid_class_ids"],
            result["invalid_boxes"],
        ]):
            all_passed = False

    print("\n" + "=" * 65)

    if all_passed:
        print("RESULT: DATASET QUALITY CHECK PASSED")
        print("All cleaned images have matching valid YOLO labels.")
    else:
        print("RESULT: ISSUES FOUND")
        print("Please review the reported problems.")

    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()