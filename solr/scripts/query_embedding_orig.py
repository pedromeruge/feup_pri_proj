import requests
from sentence_transformers import SentenceTransformer
import json
import sys

def text_to_embedding(query_data):

    text = query_data.get("query", "")
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=vector topK=30}}{embedding}",
        "fl": "id,name,score",
        "rows": 30,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    write_results_to_file(data, "debug_params2.json")

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def display_results(results):
    docs = results.get("response", {}).get("docs", [])
    if not docs:
        print("No results found.")
        return

    for doc in docs:
        print(f"* {doc.get('id')} {doc.get('name')} [score: {doc.get('score'):.2f}]")

def write_results_to_file(results, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")


def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "videogames"
    
    # Read query JSON from stdin
    try:
        query_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse input JSON. {e}")
        sys.exit(1)

    embedding = text_to_embedding(query_data)

    try:
        results = solr_knn_query(solr_endpoint, collection, embedding)
        
        # Print raw results to stdout
        print(json.dumps(results, indent=2))

    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    main()
