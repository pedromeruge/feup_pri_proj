#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

import requests


def fetch_solr_results():

    query_full = {
        "query": "",
        "params": {
            "defType": "edismax",
            "fl": "id,name,score",
            "qf": "name developers publishers genres^3 supported_languages^5 steam_description^1.5 os^5 categories^3 giantbomb_overview^1.5 characters locations specific_concepts^3 ign_review_text^1.5",
            "pf": "steam_description^5 giantbomb_overview^5 ign_review_text^5 categories^3 specific_concepts^3",
            "ps": "2",
            "rows": 30
        }
    }

    # Construct the Solr request URL
    uri = f"http://localhost:8983/solr/videogames/select"

    query_text = input("Input your videogame query:")

    query_full["query"] = query_text

    try:
        # Send the POST request to Solr
        response = requests.post(uri, json=query_full)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")
        sys.exit(1)

    # Fetch and print the results as JSON
    results = response.json()
    for i, doc in enumerate(results["response"]["docs"]):
        print(f"{i + 1}. {doc['name']} (score: {doc['score']}) (id: {doc['id']})")

if __name__ == "__main__":
  
    # Call the function with parsed arguments
    fetch_solr_results()
