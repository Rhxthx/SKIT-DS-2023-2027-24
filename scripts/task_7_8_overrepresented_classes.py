from pathlib import Path
import csv

# ============================================================
# TASK 7.8 — OVERREPRESENTED CLASSES
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "overrepresented_classes.csv"

MAXIMUM_IMAGES = 500

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
print("TASK 7.8 — OVERREPRESENTED CLASSES")
print("=" * 65)

print()
print(f"Maximum allowed images per class: {MAXIMUM_IMAGES}")
print()

overrepresented = []

for class_name, image_count in IMAGE_COUNTS.items():

    if image_count > MAXIMUM_IMAGES:
        status = "OVERREPRESENTED"
        overrepresented.append(
            (class_name, image_count)
        )
    else:
        status = "ADEQUATE"

    print(
        f"{class_name.title():<20}"
        f"{image_count:>8}  "
        f"{status}"
    )

print()
print("-" * 65)

print(
    f"Classes checked       : {len(IMAGE_COUNTS)}"
)

print(
    f"Overrepresented       : {len(overrepresented)}"
)

if overrepresented:

    print()
    print("Overrepresented classes:")

    for class_name, count in overrepresented:
        print(
            f"- {class_name.title()} : {count} images"
        )

else:

    print()
    print("Overrepresented classes: NONE")

    print(
        "All 9 selected classes are within "
        "the acceptable image range."
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
        "maximum_threshold",
        "status"
    ])

    for class_name, image_count in IMAGE_COUNTS.items():

        status = (
            "OVERREPRESENTED"
            if image_count > MAXIMUM_IMAGES
            else "ADEQUATE"
        )

        writer.writerow([
            class_name,
            image_count,
            MAXIMUM_IMAGES,
            status
        ])


print()
print("Report saved to:")
print(OUTPUT_FILE)

print()
print("=" * 65)
print("TASK 7.8 COMPLETED")
print("=" * 65)
