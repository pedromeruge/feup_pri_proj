import requests
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=vector topK=10}}{embedding}",
        "fl": "id,name,score",
        "rows": 10,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
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

def expand_query_with_llm(query_text):
    gemini_api_key = "AIzaSyByg2U8rF8Qgp_qgxxDkg_iRnABlebSvtg"
    genai.configure(api_key=gemini_api_key)
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = f"Expand the following query by about the triple of the words, without adding new ideas. This will be a query based on finding videogames, so try to expand on gaming concepts and better describing the concepts in the original prompt. Do not reply with any other words besides the expanded query. Here is the original query: {query_text}"
    response = model.generate_content(prompt)
    expanded_query = response.text.strip()
    return expanded_query

def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "videogames"
    
    query_text = input("Enter your query: ")
    print(f"OG Query: {query_text}")
    expanded_query_text = expand_query_with_llm(query_text)
    print(f"Expanded Query: {expanded_query_text}")
    
    embedding = text_to_embedding(expanded_query_text)

    try:
        results = solr_knn_query(solr_endpoint, collection, embedding)
        display_results(results)
    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    main()
