from pathlib import Path
import csv

# ============================================================
# TASK 7.4 — TRAIN VS VALIDATION DISTRIBUTION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "train_validation_distribution.csv"


TRAIN_COUNTS = {
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

VALIDATION_COUNTS = {
    "elephant": 152,
    "bear": 122,
    "tiger": 119,
    "lion": 132,
    "leopard": 148,
    "cheetah": 123,
    "brown bear": 139,
    "jaguar": 178,
    "rhinoceros": 102,
}


print("=" * 65)
print("TASK 7.4 — TRAIN VS VALIDATION DISTRIBUTION")
print("=" * 65)

print()

print(
    f"{'Class':<20}"
    f"{'Train':>10}"
    f"{'Validation':>15}"
)

print("-" * 65)

for class_name in TRAIN_COUNTS:

    print(
        f"{class_name.title():<20}"
        f"{TRAIN_COUNTS[class_name]:>10}"
        f"{VALIDATION_COUNTS[class_name]:>15}"
    )


# ============================================================
# TOTALS
# ============================================================

total_train = sum(TRAIN_COUNTS.values())
total_validation = sum(VALIDATION_COUNTS.values())
total_images = total_train + total_validation

print("-" * 65)

print(
    f"{'TOTAL':<20}"
    f"{total_train:>10}"
    f"{total_validation:>15}"
)

print()
print(f"Total train images      : {total_train}")
print(f"Total validation images : {total_validation}")
print(f"Total images            : {total_images}")


# ============================================================
# SAVE CSV
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
        "train_images",
        "validation_images",
        "total_images"
    ])

    for class_name in TRAIN_COUNTS:

        writer.writerow([
            class_name,
            TRAIN_COUNTS[class_name],
            VALIDATION_COUNTS[class_name],
            (
                TRAIN_COUNTS[class_name]
                + VALIDATION_COUNTS[class_name]
            )
        ])

    writer.writerow([
        "TOTAL",
        total_train,
        total_validation,
        total_images
    ])


print()
print("Report saved to:")
print(OUTPUT_FILE)

print()
print("=" * 65)
print("TASK 7.4 COMPLETED")
print("=" * 65)
