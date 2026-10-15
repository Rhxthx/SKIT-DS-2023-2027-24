from pathlib import Path
import csv

# ============================================================
# TASK 7.6 — MINIMUM EXAMPLES CHECK
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "minimum_examples_check.csv"

# Minimum required images per class
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
print("TASK 7.6 — MINIMUM EXAMPLES CHECK")
print("=" * 65)

print()
print(f"Minimum required images per class: {MINIMUM_IMAGES}")
print()

print(
    f"{'Class':<20}"
    f"{'Images':>10}"
    f"{'Status':>15}"
)

print("-" * 65)

below_minimum = []
passing = []

for class_name, image_count in IMAGE_COUNTS.items():

    if image_count < MINIMUM_IMAGES:
        status = "BELOW MINIMUM"
        below_minimum.append(class_name)
    else:
        status = "PASS"
        passing.append(class_name)

    print(
        f"{class_name.title():<20}"
        f"{image_count:>10}"
        f"{status:>15}"
    )


print()
print("-" * 65)

print(f"Classes checked  : {len(IMAGE_COUNTS)}")
print(f"Classes passing  : {len(passing)}")
print(f"Below minimum   : {len(below_minimum)}")

if below_minimum:
    print()
    print("Classes below minimum:")
    for class_name in below_minimum:
        print(f"- {class_name.title()}")
else:
    print()
    print("All 9 classes meet the minimum examples requirement.")


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
        "minimum_required",
        "status"
    ])

    for class_name, image_count in IMAGE_COUNTS.items():

        status = (
            "PASS"
            if image_count >= MINIMUM_IMAGES
            else "BELOW_MINIMUM"
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
print("TASK 7.6 COMPLETED")
print("=" * 65)