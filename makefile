#!make
SHELL := /bin/bash
.DEFAULT_GOAL := help
include config.env

build_and_publish:: ## Builds and publishes(GCR) docker-image to be deployed on cloud-run service.
	@cd build; \
		docker build --tag gcr.io/${project_id}/pretend_bom --file pretend_bom_dockerfile . ; \
		docker build --tag gcr.io/${project_id}/code_challenge --file code_challenge_dockerfile . ; \
		docker push gcr.io/${project_id}/pretend_bom ; \
		docker push gcr.io/${project_id}/code_challenge ;

create_services:: ## creates cloud-run service
	@gcloud run deploy pretend-bom \
		--image gcr.io/${project_id}/pretend_bom --region ${cloud_run_preferred_region} --allow-unauthenticated ; \
	gcloud run deploy code-challenge \
		--image gcr.io/${project_id}/code_challenge --region ${cloud_run_preferred_region} --allow-unauthenticated ; \
	docker run gcr.io/${project_id}/code_challenge pytest tests.py

destroy:: ## clean-up the resources
	@gcloud run services delete pretend-bom --quiet --region ${cloud_run_preferred_region} ; \
	gcloud run services delete code-challenge --quiet --region ${cloud_run_preferred_region} ;

help: ## Help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)