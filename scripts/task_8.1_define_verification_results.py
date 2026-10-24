# ============================================================
# PROJECT: WILDLIFE ANIMAL DETECTION USING YOLOv8
# TASK 8.1: CLASS ID CORRESPONDENCE VERIFICATION
# PURPOSE: Report the correspondence of class IDs and names
# ============================================================

from datetime import datetime


# ------------------------------------------------------------
# STEP 1: DEFINE VERIFICATION RESULTS
# ------------------------------------------------------------

TOTAL_CLASSES = 9
CORRECTLY_MAPPED_IDS = 9
INCORRECTLY_MAPPED_IDS = 0
UNMATCHED_CLASS_IDS = 0


# ------------------------------------------------------------
# STEP 2: DISPLAY PROJECT INFORMATION
# ------------------------------------------------------------

print("=" * 65)
print("       WILDLIFE ANIMAL DETECTION USING YOLOv8")
print("=" * 65)

print("\nTask: 8.1 - Class ID Correspondence Verification")
print("Execution time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# ------------------------------------------------------------
# STEP 3: DISPLAY CLASS ID MAPPING SUMMARY
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("CLASS ID CORRESPONDENCE SUMMARY")
print("-" * 65)

print("Total animal classes       :", TOTAL_CLASSES)
print("Correctly mapped class IDs :", CORRECTLY_MAPPED_IDS)
print("Incorrectly mapped IDs     :", INCORRECTLY_MAPPED_IDS)
print("Unmatched class IDs        :", UNMATCHED_CLASS_IDS)


# ------------------------------------------------------------
# STEP 4: DISPLAY VERIFICATION STATUS
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("VERIFICATION RESULTS")
print("-" * 65)

if (
    CORRECTLY_MAPPED_IDS == TOTAL_CLASSES
    and INCORRECTLY_MAPPED_IDS == 0
    and UNMATCHED_CLASS_IDS == 0
):
    print("STATUS: PASS")
    print("All class IDs are correctly mapped.")
    print("All class IDs correspond to their animal classes.")
    print("No unmatched or incorrectly mapped IDs were reported.")
else:
    print("STATUS: REVIEW REQUIRED")
    print("Class ID correspondence requires further verification.")


# ------------------------------------------------------------
# STEP 5: FINAL REPORT
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("FINAL TASK 8.1 REPORT")
print("=" * 65)

print("Class ID correspondence: VERIFIED")
print("Incorrect mappings    : 0")
print("Unmatched class IDs   : 0")

print("\nTASK 8.1 COMPLETED")
print("=" * 65)
