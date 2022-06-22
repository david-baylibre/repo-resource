DOCKER_PREFIX=mkorpershoek
DOCKER_NAME=repo-resource

all: docker

test:
	python -m unittest repo_resource/test_*.py

docker:
	docker build . \
		--tag "$(DOCKER_NAME):latest"

push: docker
		docker image tag ${DOCKER_NAME} ${DOCKER_PREFIX}/${DOCKER_NAME}
		docker push ${DOCKER_PREFIX}/${DOCKER_NAME}
