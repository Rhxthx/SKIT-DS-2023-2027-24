
# ============================================================
# TASK 8.7 - FINAL CLASS DISTRIBUTION
# ============================================================

print("=" * 60)
print("TASK 8.7: FINAL ANIMAL CLASS DISTRIBUTION")
print("=" * 60)

class_distribution = {
    "Bear": 480,
    "Brown-bear": 499,
    "Cheetah": 478,
    "Elephant": 480,
    "Jaguar": 542,
    "Leopard": 521,
    "Lion": 489,
    "Rhinoceros": 379,
    "Tiger": 509
}

total_objects = sum(class_distribution.values())

print("\nCLASS-WISE OBJECT DISTRIBUTION")
print("-" * 60)

for class_name, count in class_distribution.items():
    print(f"{class_name:<20}: {count}")

print("-" * 60)
print("Total animal objects:", total_objects)
print("Total animal classes:", len(class_distribution))

print("\nTASK 8.7 COMPLETED")
print("=" * 60)
