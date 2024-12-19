#!/usr/bin/env python3

import json
import sys
from pathlib import Path
import google.generativeai as genai

def expand_query(query_file, output_file):

    # Load the query parameters from the JSON file
    try:
        query_params = json.load(open(query_file))
    except FileNotFoundError:
        print(f"Error: Query file {query_file} not found.")
        sys.exit(1)

    query_text = expand_query_with_llm(query_params["query"])

    query_params["query"] = query_text

    with open(output_file, 'w') as outfile:
        json.dump(query_params, outfile, indent=2)

def expand_query_with_llm(query_text):
    gemini_api_key = "AIzaSyByg2U8rF8Qgp_qgxxDkg_iRnABlebSvtg"
    genai.configure(api_key=gemini_api_key)
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = f"Expand the following query by about the triple of the words, without adding new ideas. This will be a query based on finding videogames, so try to expand on gaming concepts and better describing the concepts in the original prompt. Do not reply with any other words besides the expanded query. Here is the original query: {query_text}"
    response = model.generate_content(prompt)
    expanded_query = response.text.strip()
    return expanded_query

if __name__ == "__main__":

    # Call the function with parsed arguments
    expand_query(sys.argv[1], sys.argv[2])
