#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path
import google.generativeai as genai
import requests

def fetch_solr_results(query_file, solr_uri, collection):
    """
    Fetch search results from a Solr instance based on the query parameters.

    Arguments:
    - query_file: Path to the JSON file containing Solr query parameters.
    - solr_uri: URI of the Solr instance (e.g., http://localhost:8983/solr).
    - collection: Solr collection name from which results will be fetched.

    Output:
    - Prints the JSON search results to STDOUT.
    """
    # Load the query parameters from the JSON file
    try:
        query_params = json.load(open(query_file))
    except FileNotFoundError:
        print(f"Error: Query file {query_file} not found.")
        sys.exit(1)

    # Construct the Solr request URL
    uri = f"{solr_uri}/{collection}/select"

    query_text = expand_query_with_llm(query_params["query"])

    query_params["query"] = query_text
    # print(query_params)
    try:
        # Send the POST request to Solr
        response = requests.post(uri, json=query_params)
        response.raise_for_status()  # Raise error if the request failed
    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")
        sys.exit(1)

    # Fetch and print the results as JSON
    results = response.json()
    print(json.dumps(results, indent=2))

def expand_query_with_llm(query_text):
    gemini_api_key = "AIzaSyByg2U8rF8Qgp_qgxxDkg_iRnABlebSvtg"
    genai.configure(api_key=gemini_api_key)
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = f"Expand the following query by about the triple of the words, without adding new ideas. This will be a query based on finding videogames, so try to expand on gaming concepts and better describing the concepts in the original prompt. Do not reply with any other words besides the expanded query. Here is the original query: {query_text}"
    response = model.generate_content(prompt)
    expanded_query = response.text.strip()
    return expanded_query

if __name__ == "__main__":
    # Set up argument parsing for the command-line interface
    parser = argparse.ArgumentParser(
        description="Fetch search results from Solr and output them in JSON format."
    )

    # Add arguments for query file, Solr URI, and collection name
    parser.add_argument(
        "--query",
        type=Path,
        required=True,
        help="Path to the JSON file containing the Solr query parameters.",
    )
    parser.add_argument(
        "--uri",
        type=str,
        default="http://localhost:8983/solr",
        help="The URI of the Solr instance (default: http://localhost:8983/solr).",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="courses",
        help="Name of the Solr collection to query (default: 'courses').",
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the function with parsed arguments
    fetch_solr_results(args.query, args.uri, args.collection)
