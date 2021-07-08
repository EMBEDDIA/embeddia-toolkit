EMBEDDIA Toolkit API wrapping EMBEDDIA API-based Services

# Running the Docker
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
After downloading all the required models the EMBEDDIA Toolkit becomes accessible via HTTP. The toolkit is usable via:

* GUI which is by default deployed at http://localhost:8090,
* and API deployed at http://localhost:8090/api/v1/.

# Dev Setup

**Clone with EMBEDDIA Submodules**

```
git clone --recursive https://git.texta.ee/texta/embeddia-toolkit.git
```

**Building & Pushing Images**

```
docker-compose build

docker-compose push
```

**Submodules**

All submodules (EMBEDDIA services) used in EMBEDDIA Toolkit are listed here: https://git.texta.ee/texta/embeddia-toolkit/-/tree/master/modules.
