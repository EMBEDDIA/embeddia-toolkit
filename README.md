# EMBEDDIA Toolkit

## Components

### Keyword Extractor - TNT-KID (Croatian, Estonian, Latvian)
A supervised method for keyword extraction using a sequence labelling approach.

Additional information: https://github.com/EMBEDDIA/tnt_kid

### Keyword Extractor - RaKUn (Multilingual)
An unsupervised method keyword extraction using graph-based approach.

Additional information: https://github.com/EMBEDDIA/RaKUn

### Named Entity Extractor (Croatian)
A supervised method for Named Entity Extractor is based on a BiLSTM with multiple types of embeddings (BERT, FastText and character).

Additional information: https://github.com/EMBEDDIA/bert-bilstm-cnn-crf-ner

### Named Entity Extractor - TEXTA MLP (Multilingual)
An hybrid method incorporating rule-based and supervised solutions for general entity extraction.

Additional information: https://pypi.org/project/texta-mlp https://git.texta.ee/texta/texta-mlp-python

### Comment Moderator - QMUL Simple BERT Model (Cross-lingual)
A supervised method for classifying texts using Multilingual BERT, fine-tuned on manually annotated Tweets in English. Can be applied to any language (but will work best on English).

Additional information: https://github.com/EMBEDDIA/comment-filter

### Comment Moderator - QMUL Multilingual BERT Model (Cross-lingual)
A supervised method for classifying texts using Multilingual BERT, fine-tuned on data in English, German, Croatian, Slovene and Estonian. Can be applied to any language (but will work best on the training languages).

Additional information: https://github.com/EMBEDDIA/comment-filter-mbert-multi

### Comment Moderator - QMUL CSEBERT Model (English, Slovenian, Croatian)
A supervised method for classifying texts using CroSloEngualBERT, fine-tuned on data in English, Croatian, and Slovene. Can be applied to any of these three languages.

Additional information: https://github.com/EMBEDDIA/comment-filter-csebert-cse

### Comment Moderator - QMUL FEBERT Model (English, Estonian)
A supervised method for classifying texts using FinEstBERT, fine-tuned on data in English and Estonian. Can be applied to those two languages (and Finnish although performance will be less good).

Additional information: https://github.com/EMBEDDIA/comment-filter-finest-bert-engee

### Comment Moderator - TEXTA BERT Model (Estonian)
A supervised method for classifying texts using Estonian BERT, fine-tuned on annotated comments in Estonian. Can be applied only to Estonian language data.

Additional information: https://pypi.org/project/texta-bert-tagger https://git.texta.ee/texta/texta-bert-tagger-python

### Article Generator
Produces short descriptive texts about the COVID-situation and Eurostat statistics.

Additional information: https://github.com/EMBEDDIA/covid-nlg https://github.com/EMBEDDIA/eurostat-nlg


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

