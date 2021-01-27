import os, sys

from google.cloud import pubsub_v1

topic_envname = 'CLOUDWORKER_TOPIC'
project_envname = 'GCP_PROJECT'
credentials_envname = 'GOOGLE_APPLICATION_CREDENTIALS'
subscription_envname = 'CLOUDWORKER_SUB'

if topic_envname in os.environ:
    topic_id = os.environ[ topic_envname ]
else:
    sys.exit( topic_envname + " is not set")

if project_envname in os.environ:
    project_id = os.environ[ project_envname ]
else:
    sys.exit( project_envname + " is not set")

if subscription_envname in os.environ:
    subscription_id = os.environ[subscription_envname]
else:
    sys.exit( subscription_envname + "is not set")

# not really necessary
if  credentials_envname not in os.environ:
    sys.exit( credentials_envname + " is not set ")

class Consumer(object):

    def Consume(object, callback ):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path( project_id, subscription_id )

        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

        with subscriber:
            try:
                # todo set timeout
                streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()


class Publisher(object): 

    @staticmethod
    def Publish(data):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path( project_id, topic_id)
        data = data.encode( "utf-8")

        #log 
        print( project_id + " " + topic_id)
        print( topic_path + " "  )

        future = publisher.publish( topic_path, data)

        # define how to test it
        result = future.result()
        print( type( result ))
        
# def implicit():
#     from google.cloud import storage

#     # If you don't specify credentials when constructing the client, the
#     # client library will look for credentials in the environment.
#     storage_client = storage.Client()

#     # Make an authenticated API request
#     buckets = list(storage_client.list_buckets())
#     print(buckets)
