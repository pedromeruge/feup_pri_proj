# Define the input and output file paths
input_file = "query4_qrels.txt"
output_file = "query4_qrels_global.txt"

# Dictionary to store unique entries based on the left number
unique_entries = {}

# Read the input file
with open(input_file, "r") as file:
    for line in file:
        left, right = line.strip().split()
        left = int(left)
        right = int(right)
        # Add to dictionary only if the left number is not already present
        if left not in unique_entries:
            unique_entries[left] = right

# Write the unique entries to the output file
with open(output_file, "w") as file:
    for left, right in unique_entries.items():
        file.write(f"{left} {right}\n")

print("Filtering complete. Check the output file.")