from pathlib import Path
import csv

# ============================================================
# TASK 7.5 — INITIAL CLASS BALANCE ANALYSIS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "initial_class_balance_analysis.csv"


# ============================================================
# DATA FROM TASK 7.2 — IMAGES PER CLASS
# ============================================================

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


# ============================================================
# DATA FROM TASK 7.3 — OBJECTS PER CLASS
# ============================================================

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


# ============================================================
# FIND HIGHEST AND LOWEST OBJECT COUNTS
# ============================================================

highest_class = max(
    OBJECT_COUNTS,
    key=OBJECT_COUNTS.get
)

lowest_class = min(
    OBJECT_COUNTS,
    key=OBJECT_COUNTS.get
)

highest_count = OBJECT_COUNTS[highest_class]
lowest_count = OBJECT_COUNTS[lowest_class]

imbalance_ratio = highest_count / lowest_count


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 65)
print("TASK 7.5 — INITIAL CLASS BALANCE ANALYSIS")
print("=" * 65)

print()
print("Class distribution:")
print()

print(
    f"{'Class':<20}"
    f"{'Images':>10}"
    f"{'Objects':>12}"
)

print("-" * 65)

for class_name in OBJECT_COUNTS:

    print(
        f"{class_name.title():<20}"
        f"{IMAGE_COUNTS[class_name]:>10}"
        f"{OBJECT_COUNTS[class_name]:>12}"
    )

print()
print("-" * 65)

print(
    f"Highest object count : "
    f"{highest_class.title()} — {highest_count}"
)

print(
    f"Lowest object count  : "
    f"{lowest_class.title()} — {lowest_count}"
)

print(
    f"Object count range   : "
    f"{lowest_count} - {highest_count}"
)

print(
    f"Imbalance ratio      : "
    f"{imbalance_ratio:.2f}"
)

print()
print("Initial assessment:")
print(
    "The 9 selected classes show a relatively moderate "
    "difference in object counts."
)

print(
    f"{lowest_class.title()} has the lowest representation, "
    f"while {highest_class.title()} has the highest."
)

print()
print(
    "No balancing action is applied at this stage. "
    "This is an initial class balance analysis."
)


# ============================================================
# SAVE CSV REPORT
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
        "object_count"
    ])

    for class_name in OBJECT_COUNTS:

        writer.writerow([
            class_name,
            IMAGE_COUNTS[class_name],
            OBJECT_COUNTS[class_name]
        ])

    writer.writerow([])
    writer.writerow([
        "Highest object count",
        highest_class,
        highest_count
    ])

    writer.writerow([
        "Lowest object count",
        lowest_class,
        lowest_count
    ])

    writer.writerow([
        "Object count range",
        f"{lowest_count}-{highest_count}"
    ])

    writer.writerow([
        "Imbalance ratio",
        f"{imbalance_ratio:.2f}"
    ])


print()
print("Report saved to:")
print(OUTPUT_FILE)

print()
print("=" * 65)
print("TASK 7.5 COMPLETED")
print("=" * 65)
