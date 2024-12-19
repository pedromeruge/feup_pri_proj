import requests
from sentence_transformers import SentenceTransformer
import json
import sys
import google.generativeai as genai

def text_to_embedding(text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    # Convert embedding to a comma-separated string
    embedding_str = ",".join(map(str, embedding))
    return embedding_str

def combined_solr_query(endpoint, collection, query_data, embedding, query_text):
    url = f"{endpoint}/{collection}/select"

    # Add the combined score calculation
    query_data["params"]["boost"] = "sum( { !knn f=vector topK=30 q='}^0.5, score^1 )"


    # Send the request to Solr
    headers = {
        "Content-Type": "application/json"
    }

    write_results_to_file(query_data, "debug_params.json")
    response = requests.post(url, json=query_data, headers=headers)
    response.raise_for_status()
    return response.json()

def expand_query_with_llm(query_text):
    gemini_api_key = "AIzaSyByg2U8rF8Qgp_qgxxDkg_iRnABlebSvtg"
    genai.configure(api_key=gemini_api_key)
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = f"Expand the following query by about the triple of the words, without adding new ideas. This will be a query based on finding videogames, so try to expand on gaming concepts and better describing the concepts in the original prompt. Do not reply with any other words besides the expanded query. Here is the original query: {query_text}"
    response = model.generate_content(prompt)
    expanded_query = response.text.strip()
    return expanded_query

def write_results_to_file(results, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")


def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "videogames"
    output_file = "results.json"  # Output file for raw results

    # Read query JSON from stdin
    try:
        query_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse input JSON. {e}")
        sys.exit(1)

    # Extract the query text
    query_text = query_data.get("query", "")

    # print(f"OG Query: {query_text}")
    # query_text = expand_query_with_llm(query_text)
    # print(f"Expanded Query: {query_text}")

    # Convert the query text into an embedding
    embedding = text_to_embedding(query_text)

    # Perform the combined query
    try:
        results = combined_solr_query(solr_endpoint, collection, query_data, embedding, query_text)
        
       # Print raw results to stdout
        print(json.dumps(results, indent=2))

    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()