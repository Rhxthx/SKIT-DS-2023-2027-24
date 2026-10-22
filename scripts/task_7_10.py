from pathlib import Path

# ============================================================
# TASK 7.10 — FINAL TASK 7 REPORT
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORT_DIR = ROOT / "reports" / "task_7"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "TASK_7_FINAL_REPORT.txt"


# ============================================================
# FINAL 9 CLASSES
# ============================================================

classes = [
    "Elephant",
    "Bear",
    "Tiger",
    "Lion",
    "Leopard",
    "Cheetah",
    "Brown Bear",
    "Jaguar",
    "Rhinoceros",
]


# ============================================================
# 7.2 — IMAGES PER CLASS
# ============================================================

image_counts = {
    "Elephant": 411,
    "Bear": 422,
    "Tiger": 435,
    "Lion": 408,
    "Leopard": 480,
    "Cheetah": 437,
    "Brown Bear": 478,
    "Jaguar": 493,
    "Rhinoceros": 352,
}


# ============================================================
# 7.3 — OBJECTS PER CLASS
# ============================================================

object_counts = {
    "Elephant": 480,
    "Bear": 499,
    "Tiger": 509,
    "Lion": 489,
    "Leopard": 521,
    "Cheetah": 478,
    "Brown Bear": 510,
    "Jaguar": 542,
    "Rhinoceros": 379,
}


# ============================================================
# 7.4 — TRAIN / VALIDATION
# ============================================================

train_counts = {
    "Elephant": 411,
    "Bear": 422,
    "Tiger": 435,
    "Lion": 408,
    "Leopard": 480,
    "Cheetah": 437,
    "Brown Bear": 478,
    "Jaguar": 493,
    "Rhinoceros": 352,
}

validation_counts = {
    "Elephant": 152,
    "Bear": 122,
    "Tiger": 119,
    "Lion": 132,
    "Leopard": 148,
    "Cheetah": 123,
    "Brown Bear": 139,
    "Jaguar": 178,
    "Rhinoceros": 102,
}


# ============================================================
# 7.5 — BALANCE ANALYSIS
# ============================================================

highest_class = max(
    object_counts,
    key=object_counts.get
)

lowest_class = min(
    object_counts,
    key=object_counts.get
)

highest_object_count = object_counts[highest_class]
lowest_object_count = object_counts[lowest_class]

imbalance_ratio = (
    highest_object_count / lowest_object_count
)


# ============================================================
# 7.6–7.8
# ============================================================

minimum_threshold = 300
maximum_threshold = 500

underrepresented = [
    class_name
    for class_name, count in image_counts.items()
    if count < minimum_threshold
]

overrepresented = [
    class_name
    for class_name, count in image_counts.items()
    if count > maximum_threshold
]


# ============================================================
# REPORT CONTENT
# ============================================================

report = []

report.append("=" * 75)
report.append("TASK 7 — FINAL CLASS DISTRIBUTION AND BALANCE REPORT")
report.append("=" * 75)

report.append("")
report.append("7.1 — FINAL CLASS SELECTION")
report.append("-" * 75)

for number, class_name in enumerate(classes, start=1):
    report.append(f"{number}. {class_name}")

report.append("")
report.append(f"Total final classes: {len(classes)}")


# ============================================================
# 7.2
# ============================================================

report.append("")
report.append("7.2 — IMAGES PER CLASS")
report.append("-" * 75)

report.append(
    f"{'Class':<20}{'Images':>10}"
)

for class_name in classes:
    report.append(
        f"{class_name:<20}"
        f"{image_counts[class_name]:>10}"
    )

report.append("")
report.append(
    f"Total images across selected class counts: "
    f"{sum(image_counts.values())}"
)


# ============================================================
# 7.3
# ============================================================

report.append("")
report.append("7.3 — OBJECTS PER CLASS")
report.append("-" * 75)

report.append(
    f"{'Class':<20}{'Objects':>10}"
)

for class_name in classes:
    report.append(
        f"{class_name:<20}"
        f"{object_counts[class_name]:>10}"
    )

report.append("")
report.append(
    f"Total objects: {sum(object_counts.values())}"
)


# ============================================================
# 7.4
# ============================================================

report.append("")
report.append("7.4 — TRAIN VS VALIDATION DISTRIBUTION")
report.append("-" * 75)

report.append(
    f"{'Class':<20}"
    f"{'Train':>10}"
    f"{'Validation':>15}"
)

for class_name in classes:
    report.append(
        f"{class_name:<20}"
        f"{train_counts[class_name]:>10}"
        f"{validation_counts[class_name]:>15}"
    )

total_train = sum(train_counts.values())
total_validation = sum(validation_counts.values())

report.append("")
report.append(f"Total train images      : {total_train}")
report.append(f"Total validation images : {total_validation}")
report.append(
    f"Total train + validation: "
    f"{total_train + total_validation}"
)


# ============================================================
# 7.5
# ============================================================

report.append("")
report.append("7.5 — INITIAL CLASS BALANCE ANALYSIS")
report.append("-" * 75)

report.append(
    f"Highest object count : "
    f"{highest_class} — {highest_object_count}"
)

report.append(
    f"Lowest object count  : "
    f"{lowest_class} — {lowest_object_count}"
)

report.append(
    f"Object count range   : "
    f"{lowest_object_count} - {highest_object_count}"
)

report.append(
    f"Imbalance ratio      : "
    f"{imbalance_ratio:.2f}"
)

report.append(
    "Initial assessment: The 9 selected classes show a "
    "relatively moderate difference in object counts."
)


# ============================================================
# 7.6
# ============================================================

report.append("")
report.append("7.6 — MINIMUM EXAMPLES CHECK")
report.append("-" * 75)

report.append(
    f"Minimum required images per class: "
    f"{minimum_threshold}"
)

report.append(
    f"Classes checked: {len(classes)}"
)

report.append(
    f"Classes passing: "
    f"{len(classes) - len(underrepresented)}"
)

report.append(
    f"Classes below minimum: "
    f"{len(underrepresented)}"
)


# ============================================================
# 7.7
# ============================================================

report.append("")
report.append("7.7 — UNDERREPRESENTED CLASSES")
report.append("-" * 75)

if underrepresented:
    for class_name in underrepresented:
        report.append(
            f"- {class_name}: "
            f"{image_counts[class_name]} images"
        )
else:
    report.append("Underrepresented classes: NONE")


# ============================================================
# 7.8
# ============================================================

report.append("")
report.append("7.8 — OVERREPRESENTED CLASSES")
report.append("-" * 75)

if overrepresented:
    for class_name in overrepresented:
        report.append(
            f"- {class_name}: "
            f"{image_counts[class_name]} images"
        )
else:
    report.append("Overrepresented classes: NONE")


# ============================================================
# 7.9
# ============================================================

report.append("")
report.append("7.9 — BALANCING DECISION")
report.append("-" * 75)

report.append(
    "No class requires balancing intervention."
)

report.append(
    "No classes will be removed."
)

report.append(
    "No classes will be duplicated."
)

report.append(
    "No oversampling is required."
)

report.append(
    "No undersampling is required."
)

report.append(
    "All 9 classes will be retained."
)

report.append(
    "Current class distribution will be preserved."
)


# ============================================================
# FINAL CONCLUSION
# ============================================================

report.append("")
report.append("FINAL TASK 7 CONCLUSION")
report.append("-" * 75)

report.append(
    "The final dataset contains 9 selected wildlife classes."
)

report.append(
    "All selected classes meet the minimum image requirement."
)

report.append(
    "No underrepresented or overrepresented classes were "
    "identified using the defined thresholds."
)

report.append(
    "The class distribution is considered suitable for "
    "proceeding without additional balancing."
)

report.append("")
report.append("=" * 75)
report.append("TASK 7 COMPLETED — 7.1 TO 7.10")
report.append("=" * 75)


# ============================================================
# SAVE REPORT
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write("\n".join(report))


# ============================================================
# DISPLAY
# ============================================================

print("\n".join(report))

print("")
print("Final report saved to:")
print(OUTPUT_FILE)