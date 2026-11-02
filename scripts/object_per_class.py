from pathlib import Path
import csv

# ============================================================
# TASK 7.3 — OBJECTS PER CLASS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "objects_per_class.csv"

OBJECT_COUNTS = {
    "elephant": 480,
    "bear": 499,
    "tiger": 509,
    "lion": 489,
    "leopard": 521,
    "cheetah": 478,
    "brown bear": 510,
    "jaguar": 542,
    "rhinoceros": 379,
}

print("=" * 60)
print("TASK 7.3 — OBJECTS PER CLASS")
print("=" * 60)

print()

for number, (class_name, count) in enumerate(
    OBJECT_COUNTS.items(), start=1
):
    print(
        f"{number}. "
        f"{class_name.title():15} : {count} objects"
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
        "object_count"
    ])

    for number, (class_name, count) in enumerate(
        OBJECT_COUNTS.items(), start=1
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
print("TASK 7.3 COMPLETED")
print("=" * 60)