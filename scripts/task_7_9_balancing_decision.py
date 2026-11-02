from pathlib import Path
import csv

# ============================================================
# TASK 7.9 — BALANCING DECISION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "balancing_decision.csv"

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

MINIMUM_IMAGES = 300
MAXIMUM_IMAGES = 500

highest_class = max(
    OBJECT_COUNTS,
    key=OBJECT_COUNTS.get
)

lowest_class = min(
    OBJECT_COUNTS,
    key=OBJECT_COUNTS.get
)

imbalance_ratio = (
    OBJECT_COUNTS[highest_class]
    / OBJECT_COUNTS[lowest_class]
)

print("=" * 65)
print("TASK 7.9 — BALANCING DECISION")
print("=" * 65)

print()
print("Analysis summary:")
print()
print(f"Classes analysed       : {len(IMAGE_COUNTS)}")
print(f"Minimum image threshold: {MINIMUM_IMAGES}")
print(f"Maximum image threshold: {MAXIMUM_IMAGES}")
print(f"Lowest object count    : {lowest_class.title()} "
      f"({OBJECT_COUNTS[lowest_class]})")
print(f"Highest object count   : {highest_class.title()} "
      f"({OBJECT_COUNTS[highest_class]})")
print(f"Object imbalance ratio : {imbalance_ratio:.2f}")

print()
print("-" * 65)

print("BALANCING DECISION")
print()
print("No class requires balancing intervention.")
print()
print("Decision:")
print("• No classes will be removed.")
print("• No classes will be duplicated.")
print("• No oversampling is required.")
print("• No undersampling is required.")
print("• All 9 classes will be retained.")
print("• Current class distribution will be preserved.")

print()
print("-" * 65)

print("FINAL DECISION: RETAIN CURRENT CLASS DISTRIBUTION")


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
        "decision",
        "result"
    ])

    writer.writerow([
        "classes_analysed",
        len(IMAGE_COUNTS)
    ])

    writer.writerow([
        "underrepresented_classes",
        "None"
    ])

    writer.writerow([
        "overrepresented_classes",
        "None"
    ])

    writer.writerow([
        "balancing_required",
        "No"
    ])

    writer.writerow([
        "oversampling_required",
        "No"
    ])

    writer.writerow([
        "undersampling_required",
        "No"
    ])

    writer.writerow([
        "classes_retained",
        "All 9"
    ])

    writer.writerow([
        "final_decision",
        "Retain current class distribution"
    ])


print()
print("Report saved to:")
print(OUTPUT_FILE)

print()
print("=" * 65)
print("TASK 7.9 COMPLETED")
print("=" * 65)
