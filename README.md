# EMBEDDIA Toolkit

## Components

Analyzer Name	Media Type	Analyzer Type	Description	Available Languages	Github link
TNT-KID Analyzer	articles	keyword extraction	A supervised method for keyword extraction using a sequence labelling approach. For training  system for new language or domain, a user needs a larger unlabelled corpus, and at least a small training corpus;	Estonian, Croatian, Latvian	https://gitlab.com/matej.martinc/tnt_kid_app https://gitlab.com/boshko.koloski/tnt_kid_app_hr https://gitlab.com/boshko.koloski/tnt_kid_app_lv
Rakun Multilingual Analyzer	articles	keyword extraction	An unsupervised method for graph-based keyword detection.	English, Slovenian	https://gitlab.com/skblaz/rakun-app-docker
TEXTA Monolongual BERT Comment Model	comments	comment filtering	A supervised method for classifying texts using BERT models.	Estonian	https://git.texta.ee/texta/texta-bert-tagger-python
EMBEDDIA Cross-lingual Comment Model	comments	comment filtering			https://github.com/mpurver/comment-filter
TEXTA MLP	articles	article processing	TEXTA MLP (Multilingual Processor) is an additional module of TEXTA created for processing and enriching textual data. Capable of processing multiple languages, it’s features include the lemmatization of text, Named Entity extraction, entity linking and more.	English, Estonian, Croatian, Lithuanian, Finnish	https://git.texta.ee/texta/texta-mlp-python
NER Analyzer	articles	named entity recognition	API for NER system based on a BiLSTM with multiple types of embeddings (BERT, FastText and character)	Croatian,Slovene, Finnish, Russian, Swedish, Latvian, Lithuanian, Estonian	https://github.com/EMBEDDIA/ULR_NER_REST
Article Generator	articles	news generation			https://github.com/ljleppan/eu-nlg-prod

## Running

Running EMBEDDIA Toolkit requires Docker, check https://docs.docker.com/get-docker/ for installation instructions.

All EMBEDDIA Toolkit components are packaged as Docker images available in our registry (https://git.texta.ee/texta/embeddia-toolkit/container_registry).

Following files from the root directory of this repository are required to run EMBEDDIA Toolkit:
* docker-compose.yml
* env.embeddia
* env.hatespeech
* env.keyword
* env.ner

File **docker-compose.yml** contains all the necessary instructions to execute the toolkit. For downloading and running the images following commands must be executed in the directory containing **docker-compose.yml**:

```
docker-compose pull
docker-compose up
```
After downloading all the required models the EMBEDDIA Toolkit becomes accessible via:

* GUI which is by default deployed at http://localhost:8090,
* and API deployed at http://localhost:8090/api/v1/.

## TEXTA Toolkit
Note that some components of the EMBEDDIA Toolkit (Dashboard & TEXTA Bert Tagger) require a running instance of TEXTA Toolkit (also packaged in Docker) with pretrained models and Elasticsearch. Information about running TEXTA Toolkit can be found at https://docs.texta.ee.

The information regarding TEXTA Toolkit is defined in file **env.embeddia** with following environment variables:

* EMBEDDIA_TEXTA_HOST
* EMBEDDIA_TEXTA_TOKEN
* EMBEDDIA_TEXTA_DASHBOARD_PROJECT
* EMBEDDIA_TEXTA_BERT_PROJECT
* EMBEDDIA_TEXTA_BERT_TAGGER

