# Makefile
SHELL := /bin/bash

.PHONY: help
help:
	@echo "Commands:"
	@echo "down       : stops all running services, removes containers and volumes."
	@echo "up         : start Docker daemon and Solr."

.PHONY: style
style:
	isort src test --atomic
	black -l 100 src test
	flake8 src test

.PHONY: down
down:
	docker stop pri_solr
	docker rm pri_solr

#create docker container, post schema and populate
.PHONY: up
up:
	docker run -p 8983:8983 --name pri_solr -v ${PWD}:/data -d solr:9 solr-precreate videogames
	sleep 6
	docker exec -it pri_solr cp /data/custom/synonyms_gaming.txt /var/solr/data/videogames/conf/
	docker exec -it pri_solr cp /data/custom/stopwords_custom.txt /var/solr/data/videogames/conf/
	docker exec -it pri_solr cp /data/lemmatizers/lemmas_spacy.txt /var/solr/data/videogames/conf/
	curl -X POST -H 'Content-type:application/json' \
	--data-binary "@${PWD}/schemas/schema_milestone2.json" \
	http://localhost:8983/solr/videogames/schema
	docker exec -it pri_solr bin/solr post -c videogames /data/merged_games_final.json

.PHONY: up_vector
up_vector:
	docker run -p 8983:8983 --name pri_solr -v ${PWD}:/data -d solr:9 solr-precreate videogames
	sleep 6
	docker exec -it pri_solr cp /data/custom/synonyms_gaming.txt /var/solr/data/videogames/conf/
	docker exec -it pri_solr cp /data/custom/stopwords_custom.txt /var/solr/data/videogames/conf/
	docker exec -it pri_solr cp /data/lemmatizers/lemmas_spacy.txt /var/solr/data/videogames/conf/
	curl -X POST -H 'Content-type:application/json' \
	--data-binary "@${PWD}/schemas/schema_vector_milestone3.json" \
	http://localhost:8983/solr/videogames/schema
	docker exec -it pri_solr bin/solr post -c videogames /data/final_embeddings_datasets/merged_games_final_bert_base_nli_mean.json

#get results for query1 from solrs
.PHONY: query1
query1:
	mkdir -p queries/query1/results
	scripts/query_solr.py --query queries/query1/query1.json --uri http://localhost:8983/solr --collection videogames > queries/query1/results/query1.txt
	cat queries/query1/results/query1.txt | scripts/solr2trec.py > queries/query1/results/query1_trec.txt

#get results for query1 from solrs
.PHONY: query1_exp
query1_exp:
	mkdir -p queries/query1/results
	scripts/query_solr.py --query queries/query1/query1_exp.json --uri http://localhost:8983/solr --collection videogames > queries/query1/results/query1.txt
	cat queries/query1/results/query1.txt | scripts/solr2trec.py > queries/query1/results/query1_trec.txt

#get results for query1 from reranking
.PHONY: query1_rr
query1_rr:
	mkdir -p queries/query1/results
	scripts/query_solr.py --query queries/query1/query1_rr.json --uri http://localhost:8983/solr --collection videogames > queries/query1/results/query1.txt
	cat queries/query1/results/query1.txt | scripts/solr2trec.py > queries/query1/results/query1_trec.txt

#get results for query1 from reranking2
.PHONY: query1_exp_rr
query1_exp_rr:
	mkdir -p queries/query1/results
	scripts/query_solr.py --query queries/query1/query1_exp_rr.json --uri http://localhost:8983/solr --collection videogames > queries/query1/results/query1.txt
	cat queries/query1/results/query1.txt | scripts/solr2trec.py > queries/query1/results/query1_trec.txt


#get results for query1 from solr with embeddings
.PHONY: query1_vector
query1_vector:
	mkdir -p queries/query1/results
	cat queries/query1/query1.json | python3 scripts/query_embedding_orig.py > queries/query1/results/query1.txt
	cat queries/query1/results/query1.txt | scripts/solr2trec.py > queries/query1/results/query1_trec.txt

#get results for query1 from solr with embeddings
# .PHONY: query1_vector2
# query1_vector2:
# 	mkdir -p queries/query1/results
# 	cat queries/query1/query1.json | python3 scripts/query_embedding.py > queries/query1/results/query1.txt
# 	cat queries/query1/results/query1.txt | scripts/solr2trec.py > queries/query1/results/query1_trec.txt

#after defining trec file, get stats for query1
.PHONY: query1_stats
query1_stats:
	cat queries/query1/query1_qrels.txt | scripts/qrels2trec.py > queries/query1/query1_qrels_trec.txt
	trec_eval queries/query1/query1_qrels_trec.txt queries/query1/results/query1_trec.txt > queries/query1/results/query1_eval_res.txt
	cat queries/query1/results/query1_trec.txt | ./scripts/plot_pr.py --qrels queries/query1/query1_qrels_trec.txt --output queries/query1/results/query1_prec_rec.png

#get results for query2 from solr
.PHONY: query2
query2:
	mkdir -p queries/query2/results
	scripts/query_solr.py --query queries/query2/query2.json --uri http://localhost:8983/solr --collection videogames > queries/query2/results/query2.txt
	cat queries/query2/results/query2.txt | scripts/solr2trec.py > queries/query2/results/query2_trec.txt

#get results for query2 with llm expansion
.PHONY: query2_exp
query2_exp:
	mkdir -p queries/query2/results
	scripts/query_solr.py --query queries/query2/query2_exp.json --uri http://localhost:8983/solr --collection videogames > queries/query2/results/query2.txt
	cat queries/query2/results/query2.txt | scripts/solr2trec.py > queries/query2/results/query2_trec.txt

#get results for query2 with reranking
.PHONY: query2_rr
query2_rr:
	mkdir -p queries/query2/results
	scripts/query_solr.py --query queries/query2/query2_rr.json --uri http://localhost:8983/solr --collection videogames > queries/query2/results/query2.txt
	cat queries/query2/results/query2.txt | scripts/solr2trec.py > queries/query2/results/query2_trec.txt

#get results for query2 with reranking2
.PHONY: query2_rr
query2_exp_rr:
	mkdir -p queries/query2/results
	scripts/query_solr.py --query queries/query2/query2_exp_rr.json --uri http://localhost:8983/solr --collection videogames > queries/query2/results/query2.txt
	cat queries/query2/results/query2.txt | scripts/solr2trec.py > queries/query2/results/query2_trec.txt

#get results for query1 from solr with embeddings
.PHONY: query2_vector
query2_vector:
	mkdir -p queries/query2/results
	cat queries/query2/query2.json | python3 scripts/query_embedding_orig.py > queries/query2/results/query2.txt
	cat queries/query2/results/query2.txt | scripts/solr2trec.py > queries/query2/results/query2_trec.txt

#after defining trec file, get stats for query2
.PHONY: query2_stats
query2_stats:
	cat queries/query2/query2_qrels.txt | scripts/qrels2trec.py > queries/query2/query2_qrels_trec.txt
	trec_eval queries/query2/query2_qrels_trec.txt queries/query2/results/query2_trec.txt > queries/query2/results/query2_eval_res.txt
	cat queries/query2/results/query2_trec.txt | ./scripts/plot_pr.py --qrels queries/query2/query2_qrels_trec.txt --output queries/query2/results/query2_prec_rec.png

#get results for query3 from solr
.PHONY: query3
query3:
	mkdir -p queries/query3/results
	scripts/query_solr.py --query queries/query3/query3.json --uri http://localhost:8983/solr --collection videogames > queries/query3/results/query3.txt
	cat queries/query3/results/query3.txt | scripts/solr2trec.py > queries/query3/results/query3_trec.txt

#get results for query3 from solr
.PHONY: query3_exp
query3_exp:
	mkdir -p queries/query3/results
	scripts/query_solr.py --query queries/query3/query3_exp.json --uri http://localhost:8983/solr --collection videogames > queries/query3/results/query3.txt
	cat queries/query3/results/query3.txt | scripts/solr2trec.py > queries/query3/results/query3_trec.txt

#get results for query3 with reranking
.PHONY: query3_rr
query3_rr:
	mkdir -p queries/query3/results
	scripts/query_solr.py --query queries/query3/query3_rr.json --uri http://localhost:8983/solr --collection videogames > queries/query3/results/query3.txt
	cat queries/query3/results/query3.txt | scripts/solr2trec.py > queries/query3/results/query3_trec.txt

#get results for query3 with reranking
.PHONY: query3_exp_rr
query3_exp_rr:
	mkdir -p queries/query3/results
	scripts/query_solr.py --query queries/query3/query3_exp_rr.json --uri http://localhost:8983/solr --collection videogames > queries/query3/results/query3.txt
	cat queries/query3/results/query3.txt | scripts/solr2trec.py > queries/query3/results/query3_trec.txt

#get results for query1 from solr with embeddings
.PHONY: query3_vector
query3_vector:
	mkdir -p queries/query3/results
	cat queries/query3/query3.json | python3 scripts/query_embedding_orig.py > queries/query3/results/query3.txt
	cat queries/query3/results/query3.txt | scripts/solr2trec.py > queries/query3/results/query3_trec.txt

#after defining trec file, get stats for query3
.PHONY: query3_stats
query3_stats:
	cat queries/query3/query3_qrels.txt | scripts/qrels2trec.py > queries/query3/query3_qrels_trec.txt
	trec_eval queries/query3/query3_qrels_trec.txt queries/query3/results/query3_trec.txt > queries/query3/results/query3_eval_res.txt
	cat queries/query3/results/query3_trec.txt | ./scripts/plot_pr.py --qrels queries/query3/query3_qrels_trec.txt --output queries/query3/results/query3_prec_rec.png

#get results for query4 from solr
.PHONY: query4
query4:
	mkdir -p queries/query4/results
	scripts/query_solr.py --query queries/query4/query4.json --uri http://localhost:8983/solr --collection videogames > queries/query4/results/query4.txt
	cat queries/query4/results/query4.txt | scripts/solr2trec.py > queries/query4/results/query4_trec.txt

#get results for query4 from solr
.PHONY: query4_exp
query4_exp:
	mkdir -p queries/query4/results
	scripts/query_solr.py --query queries/query4/query4_exp.json --uri http://localhost:8983/solr --collection videogames > queries/query4/results/query4.txt
	cat queries/query4/results/query4.txt | scripts/solr2trec.py > queries/query4/results/query4_trec.txt

#get results for query4 from solr
.PHONY: query4_rr
query4_rr:
	mkdir -p queries/query4/results
	scripts/query_solr.py --query queries/query4/query4_rr.json --uri http://localhost:8983/solr --collection videogames > queries/query4/results/query4.txt
	cat queries/query4/results/query4.txt | scripts/solr2trec.py > queries/query4/results/query4_trec.txt

#get results for query4 from solr
.PHONY: query4_exp_rr
query4_exp_rr:
	mkdir -p queries/query4/results
	scripts/query_solr.py --query queries/query4/query4_exp_rr.json --uri http://localhost:8983/solr --collection videogames > queries/query4/results/query4.txt
	cat queries/query4/results/query4.txt | scripts/solr2trec.py > queries/query4/results/query4_trec.txt

#get results for query1 from solr with embeddings
.PHONY: query4_vector
query4_vector:
	mkdir -p queries/query4/results
	cat queries/query4/query4.json | python3 scripts/query_embedding_orig.py > queries/query4/results/query4.txt
	cat queries/query4/results/query4.txt | scripts/solr2trec.py > queries/query4/results/query4_trec.txt

#after defining trec file, get stats for query4
.PHONY: query4_stats
query4_stats:
	cat queries/query4/query4_qrels.txt | scripts/qrels2trec.py > queries/query4/query4_qrels_trec.txt
	trec_eval queries/query4/query4_qrels_trec.txt queries/query4/results/query4_trec.txt > queries/query4/results/query4_eval_res.txt
	cat queries/query4/results/query4_trec.txt | ./scripts/plot_pr.py --qrels queries/query4/query4_qrels_trec.txt --output queries/query4/results/query4_prec_rec.png

