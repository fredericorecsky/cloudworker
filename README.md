# cloudworker
read a stream of commands and run it


## Building on your gcp project

Fork this repo and connect the gcp to it, build a trigger or using terraform:

    resource "google_cloudbuild_trigger" "trigger" {
    provider = google-beta
    
    name = "givenname"
    description = "Some description"

    github {   
        owner = "your github username"
        name = "cloudworker"
        push {
            branch = "main"            
        }
    }

    filename = "cloudbuild.yaml"
}

## Scheduling on gcp scheduler 

You can do it on the gcp cloud console or with ioc, the exemple above is with terraform

Terraform doc link: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_scheduler_job

    resource "google_pubsub_topic" "topic" {
        name = "job-topic"
    }

    resource "google_cloud_scheduler_job" "job" {
        name        = "test-job"
        description = "test job"
        schedule    = "*/2 * * * *"

        pubsub_target {
            # topic.id is the topic's full resource name.
            topic_name = google_pubsub_topic.topic.id
            data       = base64encode("test")
        }
    }