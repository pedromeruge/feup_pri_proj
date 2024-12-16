import json
import sys 
# File paths
response_file = f"../queries/query{sys.argv[1]}/results/query{sys.argv[1]}.txt"  # First file containing JSON data
reference_file = f"global_qrels/query{sys.argv[1]}_qrels_global.txt"  # Second file with left-right column values
output_file = f"../queries/query{sys.argv[1]}/query{sys.argv[1]}_qrels.txt"  # File to write the result

# Load the reference file into a dictionary
reference_dict = {}
with open(reference_file, "r") as ref_file:
    for line in ref_file:
        left, right = line.strip().split()
        reference_dict[left] = right

# Load the response file and extract "id" values
with open(response_file, "r") as resp_file:
    response_data = json.load(resp_file)
    ids = [doc["id"] for doc in response_data["response"]["docs"]]

# Prepare the output lines
output_lines = []
to_fill_ids = []
for id_ in ids:
    if id_ in reference_dict:
        output_lines.append(f"{id_} {reference_dict[id_]}")
    else:
        output_lines.append(f"{id_} ")
        to_fill_ids.append(id_)

# Write the results to the output file
with open(output_file, "w") as out_file:
    out_file.write("\n".join(output_lines))

print(f"Output written to {output_file}")
print(f"Must fill the following entries:")
for id_ in to_fill_ids:
    print(id_)