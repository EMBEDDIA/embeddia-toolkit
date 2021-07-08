# EMBEDDIA Toolkit

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

