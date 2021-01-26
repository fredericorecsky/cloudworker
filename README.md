# cloudworker
read a stream of commands and run it




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