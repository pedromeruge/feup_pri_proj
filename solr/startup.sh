#!/bin/bash

# First the following command has to be run in directory feup_pri_proj:
docker run -p 8983:8983 --name pri_solr -v ${PWD}/solr:/data -d solr:9 solr-precreate videogames
sleep 3
# Schema definition via API, from schema.json inside container
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@${PWD}/solr/schema.json" \
    http://localhost:8983/solr/videogames/schema

# Populate collection using mapped path inside container.
docker exec -it pri_solr bin/solr post -c videogames /data/merged_games_final.json

# Other commands:
## to delete an existent core:
## docker exec pri_solr bin/solr delete -c videogames