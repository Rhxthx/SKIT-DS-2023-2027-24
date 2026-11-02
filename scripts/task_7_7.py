from pathlib import Path
import csv

# ============================================================
# TASK 7.7 — UNDERREPRESENTED CLASSES
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "underrepresented_classes.csv"

MINIMUM_IMAGES = 300

IMAGE_COUNTS = {
    "elephant": 411,
    "bear": 422,
    "tiger": 435,
    "lion": 408,
    "leopard": 480,
    "cheetah": 437,
    "brown bear": 478,
    "jaguar": 493,
    "rhinoceros": 352,
}

print("=" * 65)
print("TASK 7.7 — UNDERREPRESENTED CLASSES")
print("=" * 65)

print()
print(f"Minimum image threshold: {MINIMUM_IMAGES}")
print()

underrepresented = []

for class_name, image_count in IMAGE_COUNTS.items():

    if image_count < MINIMUM_IMAGES:
        underrepresented.append(
            (class_name, image_count)
        )

if underrepresented:

    print("Underrepresented classes:")
    print()

    for class_name, count in underrepresented:
        print(
            f"- {class_name.title()} : {count} images"
        )

else:

    print("Underrepresented classes: NONE")
    print()
    print(
        "All 9 selected classes have at least "
        f"{MINIMUM_IMAGES} images."
    )

print()
print("-" * 65)
print(f"Classes checked       : {len(IMAGE_COUNTS)}")
print(f"Underrepresented      : {len(underrepresented)}")

lowest_class = min(
    IMAGE_COUNTS,
    key=IMAGE_COUNTS.get
)

highest_class = max(
    IMAGE_COUNTS,
    key=IMAGE_COUNTS.get
)

print(
    f"Lowest representation : "
    f"{lowest_class.title()} "
    f"({IMAGE_COUNTS[lowest_class]} images)"
)

print(
    f"Highest representation: "
    f"{highest_class.title()} "
    f"({IMAGE_COUNTS[highest_class]} images)"
)


# ============================================================
# SAVE REPORT
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "class_name",
        "image_count",
        "minimum_threshold",
        "status"
    ])

    for class_name, image_count in IMAGE_COUNTS.items():

        status = (
            "UNDERREPRESENTED"
            if image_count < MINIMUM_IMAGES
            else "ADEQUATE"
        )

        writer.writerow([
            class_name,
            image_count,
            MINIMUM_IMAGES,
            status
        ])


print()
print("Report saved to:")
print(OUTPUT_FILE)

print()
print("=" * 65)
print("TASK 7.7 COMPLETED")
print("=" * 65)