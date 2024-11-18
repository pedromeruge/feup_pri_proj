# Instructions to use solr
Assuming:
- your "solr/startup.sh" script works correctly
- You have the file "solr/merged_games_final.json" obtained from unzipping the "solr/merged_games_final.json.zip"

## Setup
First we create the docker container with solr, load the schema and populate a core with our dataset.
Run inside the "solr/" folder:
```
make up
```
## Run query N
### Send query N to solr
Then we send query number {N} (1 to 4) to solr, and get the top 30 results.
Run inside the "solr/" folder:
```
make query{N}
```
For example, to run query 1 you can run "make query1"
### Evaluate results
The results of the query will be stored in the file "solr/queries/query{N}/results/query{N}.txt"
Based on the information there, for all 30 results obtained, we judge their relevance, and create a file in path "solr/queries/query{N}/query{N}_qrels.txt" where we write the document id and if it is relevant or not (relevant=1, not relevant=0), like this:
```
1062140 1
1070710 1
1186400 1
336240 0
256460 1
1290000 1
726830 0
...
```
Actually, we can just write  in this file the documents that are relevant (aka that have a 1 in front), but for better keeping track of which files have been evaluated already we include also the ones that are not relevant. For example, for the first section shown above, we could just write:
```
1062140 1
1070710 1
1186400 1
256460 1
1290000 1
...
```
### Obtain stats for query N
After writting the qrels file above, we can analyze the quality of our query {N} results.
Run inside the "solr/" folder:
```
make query{N}_stats
```
This will create:
-  a file with several statistics in path "solr/queries/query{N}/results/query{N}_eval_res.txt". 
    - "provides key evaluation metrics such as Mean Average Precision (MAP), Precision at different cut-off levels, and Interpolated Precision-Recall curves, among others."
- An image with an interpolated 11-point Precision-Recall curve in path "solr/queries/query{N}/results/query{N}_prec_rec.png". 
    - "assess how well your system balances precision and recall at different recall levels, helping you understand the trade-offs of different search configurations."

## Deletion
If at any time we want to delete your docker container because a schema was updated, or for any other reason
Run inside the "solr/" folder:
```
make down
```
This can be followed by the command in topic "Setup" to repeat the setup again
