## Approach

The general approach to the code-challenge is to develop Python FastApi endpoint to display the requested whether details.
As BOM endpoint is not working via programmatically.I did the below
* Get the latest content and saved to a file.
* Exposed this JSON as on other endpoint.

I have used GCP cloud-run services to deploy the docker-images. We have makefile to orchestrate the flow.

`make build_and_publish`: Builds docker images for both pretending bom endpoint and actual code-challege web service and publishes them to GCR
`make create_services`: Deploys the above built images on to GCP cloud-run service and perform basic testing
`make destroy`: deletes GCP cloud-run services.

Currently both the images got deployed in my personal GCP project and running as cloud-run services. Once deployment is done we will do very basic testing.

[web-service-url](https://code-challenge-7moui6f4lq-km.a.run.app/)