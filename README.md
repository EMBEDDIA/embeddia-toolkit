EMBEDDIA Toolkit API wrapping EMBEDDIA API-based Services

# Running the Docker
Running EMBEDDIA Toolkit requires Docker, check https://docs.docker.com/get-docker/ for installation instructions.

All EMBEDDIA Toolkit components are packaged as Docker images. For downloading and running the images following commands must be executed:

```
docker-compose pull
docker-compose up
```

# Accessing the EMBEDDIA Toolkit
EMBEDDIA Toolkit is usable via GUI which is by default deployed at http://localhost:8090. The API of the toolkit is accessible at http://localhost:8090/api/v1/.


# Container Registry
https://git.texta.ee/texta/embeddia-toolkit/container_registry

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
