
import sys

# File paths
reference_file = f"global_qrels/query{sys.argv[1]}_qrels_global.txt" # File with filled missing entries
output_file = f"../queries/query{sys.argv[1]}/query{sys.argv[1]}_qrels.txt"  # Global qrels file to update

# Read the existing reference file into a dictionary
reference_dict = {}
with open(reference_file, "r") as ref_file:
    for line in ref_file:
        left, right = line.strip().split()
        reference_dict[left] = right

# Read the output file and identify new entries
new_entries = []
with open(output_file, "r") as out_file:
    for line in out_file:
        left, right = line.strip().split()
        if left not in reference_dict:  # Check if the entry is new
            # Append the new entry to the list (treat empty as "0" or any placeholder)
            new_entries.append(f"{left} {right if right else '0'}")

# Append the new entries to the reference file
with open(reference_file, "a") as ref_file:
    for entry in new_entries:
        ref_file.write(f"{entry}\n")

print(f"New entries added to {reference_file}:")
for entry in new_entries:
    print(entry)