REVISION := $(shell git rev-parse --short HEAD)
DOCKER_IMAGE_NAME = cr.yandex/crpiaib4oh72mqruk1f3/fatsapi:$(REVISION)

build:
	docker build --platform linux/amd64 -t $(DOCKER_IMAGE_NAME) .

push:
	docker push $(DOCKER_IMAGE_NAME)

run:
    docker run --rm -e PORT=8080 -p 8080:8080 $(DOCKER_IMAGE_NAME)
