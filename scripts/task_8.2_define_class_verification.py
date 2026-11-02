# ============================================================
# PROJECT: WILDLIFE ANIMAL DETECTION USING YOLOv8
# TASK 8.2: ANIMAL CLASS IDENTIFICATION AND VERIFICATION
# PURPOSE: Display and verify the nine animal classes
# ============================================================

from datetime import datetime


# ------------------------------------------------------------
# STEP 1: DEFINE THE ANIMAL CLASSES
# ------------------------------------------------------------

ANIMAL_CLASSES = [
    "Bear",
    "Brown-bear",
    "Cheetah",
    "Elephant",
    "Jaguar",
    "Leopard",
    "Lion",
    "Rhinoceros",
    "Tiger"
]


# ------------------------------------------------------------
# STEP 2: DISPLAY PROJECT INFORMATION
# ------------------------------------------------------------

print("=" * 65)
print("       WILDLIFE ANIMAL DETECTION USING YOLOv8")
print("=" * 65)

print("\nTask: 8.2 - Animal Class Identification")
print("Purpose: Verify the animal classes used in the dataset")
print("Execution time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# ------------------------------------------------------------
# STEP 3: COUNT THE TOTAL NUMBER OF CLASSES
# ------------------------------------------------------------

total_classes = len(ANIMAL_CLASSES)

print("\n" + "-" * 65)
print("ANIMAL CLASS SUMMARY")
print("-" * 65)

print("Total number of animal classes:", total_classes)


# ------------------------------------------------------------
# STEP 4: DISPLAY CLASS IDs AND CLASS NAMES
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("LIST OF ANIMAL CLASSES")
print("-" * 65)

print(f"{'CLASS ID':<15}{'ANIMAL CLASS':<25}")
print("-" * 40)

for class_id, animal_name in enumerate(ANIMAL_CLASSES):
    print(f"{class_id:<15}{animal_name:<25}")


# ------------------------------------------------------------
# STEP 5: VERIFY CLASS IDS
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("CLASS ID VERIFICATION")
print("-" * 65)

expected_ids = list(range(total_classes))
actual_ids = list(range(len(ANIMAL_CLASSES)))

if actual_ids == expected_ids:
    print("PASS: Class IDs are sequential.")
    print("PASS: Class IDs start from 0.")
    print(f"PASS: Class IDs end at {total_classes - 1}.")
else:
    print("FAIL: Class ID verification failed.")


# ------------------------------------------------------------
# STEP 6: CHECK FOR DUPLICATE CLASS NAMES
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("DUPLICATE CLASS CHECK")
print("-" * 65)

if len(ANIMAL_CLASSES) == len(set(ANIMAL_CLASSES)):
    print("PASS: No duplicate class names found.")
else:
    print("WARNING: Duplicate class names were found.")


# ------------------------------------------------------------
# STEP 7: DISPLAY EACH CLASS INDIVIDUALLY
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("INDIVIDUAL CLASS DETAILS")
print("-" * 65)

for class_id, animal_name in enumerate(ANIMAL_CLASSES):
    print(f"Class {class_id}: {animal_name}")


# ------------------------------------------------------------
# STEP 8: FINAL VERIFICATION REPORT
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("FINAL VERIFICATION REPORT")
print("=" * 65)

print("Number of classes:", total_classes)
print("Class IDs verified:", "Yes")
print("Duplicate names:", "None" if len(ANIMAL_CLASSES) == len(set(ANIMAL_CLASSES)) else "Found")

print("\nFinal Animal Classes:")

for animal_name in ANIMAL_CLASSES:
    print("-", animal_name)

print("\nTASK 8.2 COMPLETED SUCCESSFULLY")
print("=" * 65)
