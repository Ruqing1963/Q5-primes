import sys

# Capacity for 12,000+ digit strings
sys.set_int_max_str_digits(300000)

# 2500 digits base
base_n = int("1" + "0" * 2499)

print("Opening concentrate file...")
try:
    with open("survivor_offsets.txt", "r") as f:
        offsets = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("Error: survivor_offsets.txt not found.")
    sys.exit(1)

print(f"Refining {len(offsets)} diamond-grade targets...")
with open("pfgw_targets.txt", "w") as out:
    for offset in offsets:
        n = base_n + int(offset)
        # Q(n) = n^5 - (n-1)^5
        qn = (n**5) - ((n-1)**5)
        # Write only the number, ensuring no extra spaces or hidden characters
        out.write(f"{str(qn).strip()}\n")

print("Success: pfgw_targets.txt is optimized for PFGW.")
