from pathlib import Path
import csv

# ============================================================
# TASK 7.1 — SELECT FINAL CLASSES
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "final_selected_classes.csv"


# ------------------------------------------------------------
# FINAL 9 CLASSES SELECTED FOR TASK 7
# ------------------------------------------------------------

FINAL_CLASSES = [
    "elephant",
    "bear",
    "tiger",
    "lion",
    "leopard",
    "cheetah",
    "brown bear",
    "jaguar",
    "rhinoceros",
]


# ------------------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------------------

print("=" * 60)
print("TASK 7.1 — FINAL CLASS SELECTION")
print("=" * 60)

print()
print("Final selected classes:")
print()

for number, class_name in enumerate(FINAL_CLASSES, start=1):
    print(f"{number}. {class_name.title()}")


# ------------------------------------------------------------
# SAVE CSV REPORT
# ------------------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "class_number",
        "class_name"
    ])

    for number, class_name in enumerate(FINAL_CLASSES, start=1):
        writer.writerow([
            number,
            class_name
        ])


# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print()
print("-" * 60)
print(f"Total final classes: {len(FINAL_CLASSES)}")

print()
print("Report saved to:")
print(OUTPUT_FILE)

print()
print("=" * 60)
print("TASK 7.1 COMPLETED")
print("=" * 60)
