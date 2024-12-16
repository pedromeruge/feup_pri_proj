import sys
import json
from sentence_transformers import SentenceTransformer

#To use, run inside folder solr/ like this: cat merged_games_final.json | python3 scripts/get_embeddings.py > merged_games_embeddings_final.json

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    # Read JSON from STDIN
    data = json.load(sys.stdin)

    # Update each document in the JSON data
    for document in data:
        combined_text = ""
        combined_text += " " + document.get("steam_description", "")
        combined_text += " " + str(document.get("giantbomb_overview", ""))
        combined_text += " " + str(document.get("ign_review_text", ""))

        document["vector"] = get_embedding(combined_text)

    # Output updated JSON to STDOUT
    json.dump(data, sys.stdout, indent=4, ensure_ascii=False)
