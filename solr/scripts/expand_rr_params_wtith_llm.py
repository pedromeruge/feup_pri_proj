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

    query_rqq_text = expand_query_with_llm(query_params["query"])

    query_params["params"]["rq"] = "{!rerank reRankDocs=100 reRankQuery=$rqq reRankWeight=3.0}"
    query_params["params"]["rqq"] = query_rqq_text

    with open(output_file, 'w') as outfile:
        json.dump(query_params, outfile, indent=2)

def expand_query_with_llm(query_text):
    gemini_api_key = "AIzaSyByg2U8rF8Qgp_qgxxDkg_iRnABlebSvtg"
    genai.configure(api_key=gemini_api_key)
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = (
        f"I want to find the best parameters to put in a Solr query for a video game search engine. "
        f"The user's query is the following: {query_text}. "
        f"This is the format of the query I am sending to the API:\n"
        f'{{\n'
        f'  "query": "{query_text}",\n'
        f'  "params": {{\n'
        f'    "rqq": "field_to_fill",\n'
        f'    "rows": 30\n'
        f'  }}\n'
        f'}}\n'
        f"Also, this is the schema i am running for this solr query:\n"
        
        f"Based on the user input query text, I want you to define an expression to put in the "
        f"reranking query field of this query (aka 'rqq') to obtain the best reordering of documents. "
        f"I want you to focus on boosting specific words or expressions that you believe are more relevant to express the user's intent. "
        f"So you can get a better understanding of which fields are more relevant or not in my dataset, here is an example of a document in my collection:\n"
           f"Here is an example video game document:\n"
        f"{{\n"
        f'  "name": "Blood Bowl 2",\n'
        f'  "required_age": 0,\n'
        f'  "price": 19.99,\n'
        f'  "developers": ["Cyanide Studios"],\n'
        f'  "publishers": ["Nacon"],\n'
        f'  "genres": ["Sports", "Strategy"],\n'
        f'  "supported_languages": ["English", "French", "German", "Polish", "Russian", "Spanish - Spain"],\n'
        f'  "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/236690/header.jpg?t=1654007385",\n'
        f'  "steam_description": "{("TOUCHDOWN! Blood Bowl 2 smashes Warhammer and American football together, in an explosive cocktail of turn-based strategy, humour and brutality, adapted from Games Workshop’s famous boardgame. "[:500] + "...")}",\n'
        f'  "os": ["mac", "windows"],\n'
        f'  "avg_sales": 750000,\n'
        f'  "steam_upvotes": 6072,\n'
        f'  "steam_downvotes": 1684,\n'
        f'  "release_date": "2015-09-22T00:00:00Z",\n'
        f'  "categories": ["Action", "Blood", "Board Game", "Dark Humor", "Difficult", "Fantasy", "Football", "Full controller support", "Funny", "Games Workshop"],\n'
        f'  "giantbomb_overview": "{("Blood Bowl 2 is a turn-based strategy and sports game based in the Warhammer Fantasy universe with added RPG elements. "[:500] + "...")}",\n'
        f'  "ign_review_text": "{("Throwing together the wild, violent, irreverent world of Warhammer Fantasy and good ol’ American football is a pairing on par with peanut butter and chocolate, Joss Whedon and The Avengers, or Commander Shepard quotes and the Internet. "[:500] + "...")}",\n'
        f'  "ign_score": "7.8"\n'
        f"}}"
        f"Answer me with just the exact string expression to put in the rqq field as an answer. Don't include any newlines or tabs in the answer string"
    )

    response = model.generate_content(prompt)
    expanded_query = response.text.strip()
    expanded_query.replace('\n', '').replace('\t', '')
    return expanded_query

if __name__ == "__main__":

    # Call the function with parsed arguments
    expand_query(sys.argv[1], sys.argv[2])
