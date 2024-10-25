#!/bin/bash

# First the following command has to be run inside feup_pri_proj/datasets:
# docker run -p 8983:8983 --name pri_solr -v ${PWD}:/data -d solr:9 solr-precreate videogames

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./simple_schema.json" \
    http://localhost:8983/solr/videogames/schema

# Populate collection using mapped path inside container.
docker exec -it pri_solr bin/post -c videogames /data/merged_games_final.json
