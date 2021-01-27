APP = cloudworker

IMAGE ?= $(APP)

GOOGLE_APPLICATION_CREDENTIALS ?= "./credential.json"
GCP_PROJECT ?= "gcp_project"
CLOUDWORKER_TOPIC ?= "cloudworker-topic"
CLOUDWORKER_SUB ?= "cloudworker-sub"

run:
	export CLOUDWORKER_TOPIC=$(CLOUDWORKER_TOPIC) && \
	export GCP_PROJECT=$(GCP_PROJECT) && \
	export GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) && \
	export CLOUDWORKER_SUB=$(CLOUDWORKER_SUB) && \
	python3 cloudworker.py

stub:
	export CLOUDWORKER_TOPIC=$(CLOUDWORKER_TOPIC) && \
	export GCP_PROJECT=$(GCP_PROJECT) && \
	export GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) && \
	export CLOUDWORKER_SUB=$(CLOUDWORKER_SUB) && \
	python3 stub.py

create-topic:
	gcloud pubsub topics create $(CLOUDWORKER_TOPIC)

create-subscription:
	gcloud pubsub subscriptions create $(CLOUDWORKER_SUB) --topic $(CLOUDWORKER_TOPIC)

requirements:
	pip freeze > requirements.txt

build-docker:
	docker build -t $(IMAGE):latest .

run-docker:
	docker run \
	-e CLOUDWORKER_TOPIC=$(CLOUDWORKER_TOPIC) \
	-e GCP_PROJECT=$(GCP_PROJECT) \
	-e CLOUDWORKER_SUB=$(CLOUDWORKER_SUB) \
	-v $(GOOGLE_APPLICATION_CREDENTIALS):$(GOOGLE_APPLICATION_CREDENTIALS):ro \
	-e GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) \
	-it --rm --name $(APP) $(IMAGE) 

cloud-build:
	gcloud builds submit --config cloudbuild.yaml .(venv) 

clean:
	gcloud pubsub subscriptions delete $(CLOUDWORKER_SUB) && \
  	gcloud pubsub topics delete $(CLOUDWORKER_TOPIC)
