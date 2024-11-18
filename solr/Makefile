# Makefile
SHELL := /bin/bash

.PHONY: help
help:
	@echo "Commands:"
	@echo "style      : runs style formatting."
	@echo "down       : stops all running services, removes containers and volumes."
	@echo "up         : start Docker daemon and Solr."
	@echo "schema     : update schema using docker/data/schema.json."
	@echo "populate   : populate Solr using docker/data/data.json."
	@echo "trec_eval  : download trec_eval source code and compile it."
	@echo "test       : run unit tests."

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
	sleep 4
	curl -X POST -H 'Content-type:application/json' \
	--data-binary "@${PWD}/schemas/schema.json" \
	http://localhost:8983/solr/videogames/schema
	docker exec -it pri_solr bin/solr post -c videogames /data/merged_games_final.json

#get results for query1 from solr
.PHONY: query1
query1:
	scripts/query_solr.py --query queries/query1/query1.json --uri http://localhost:8983/solr --collection videogames > queries/query1/results/query1.txt
	cat queries/query1/results/query1.txt | scripts/solr2trec.py > queries/query1/results/query1_trec.txt

#after defining trec file, get stats for query1
.PHONY: query1_stats
query1_stats:
	cat queries/query1/query1_qrels.txt | scripts/qrels2trec.py > queries/query1/query1_qrels_trec.txt
	trec_eval queries/query1/query1_qrels_trec.txt queries/query1/results/query1_trec.txt > queries/query1/results/query1_eval_res.txt
	cat queries/query1/results/query1_trec.txt | ./scripts/plot_pr.py --qrels queries/query1/query1_qrels_trec.txt --output queries/query1/results/query1_prec_rec.png

#get results for query2 from solr
.PHONY: query2
query2:
	scripts/query_solr.py --query queries/query2/query2.json --uri http://localhost:8983/solr --collection videogames > queries/query2/results/query2.txt
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
	scripts/query_solr.py --query queries/query3/query3.json --uri http://localhost:8983/solr --collection videogames > queries/query3/results/query3.txt
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
	scripts/query_solr.py --query queries/query4/query4.json --uri http://localhost:8983/solr --collection videogames > queries/query4/results/query4.txt
	cat queries/query4/results/query4.txt | scripts/solr2trec.py > queries/query4/results/query4_trec.txt

#after defining trec file, get stats for query4
.PHONY: query4_stats
query4_stats:
	cat queries/query4/query_qrels.txt | scripts/qrels2trec.py > queries/query4/query4_qrels_trec.txt
	trec_eval queries/query4/query4_qrels_trec.txt queries/query4/results/query4_trec.txt > queries/query4/results/query4_eval_res.txt
	cat queries/query4/results/query4_trec.txt | ./scripts/plot_pr.py --qrels queries/query4/query4_qrels_trec.txt --output queries/query4/results/query4_prec_rec.png

