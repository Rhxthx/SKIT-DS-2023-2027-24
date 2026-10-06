from pathlib import Path
import csv

# ============================================================
# TASK 7.2 — COUNT IMAGES PER CLASS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "images_per_class.csv"

TOTAL_IMAGES = 3916

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

print("=" * 60)
print("TASK 7.2 — IMAGES PER CLASS")
print("=" * 60)

print()
print(f"Total images: {TOTAL_IMAGES}")
print()

for number, (class_name, count) in enumerate(
    IMAGE_COUNTS.items(), start=1
):
    print(
        f"{number}. "
        f"{class_name.title():15} : {count}"
    )

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "class_number",
        "class_name",
        "image_count"
    ])

    for number, (class_name, count) in enumerate(
        IMAGE_COUNTS.items(), start=1
    ):
        writer.writerow([
            number,
            class_name,
            count
        ])

print()
print("Report saved to:")
print(OUTPUT_FILE)

print()
print("=" * 60)
print("TASK 7.2 COMPLETED")
print("=" * 60)
