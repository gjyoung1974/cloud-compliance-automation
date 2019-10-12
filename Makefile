all: build

IMAGE := example.com/acme-compliance-jobs:latest

build:
	docker build --rm --tag $(IMAGE) .

