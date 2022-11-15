import os
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.cloud import pubsub_v1

host= os.environ['api-host']
project_id = os.environ['proyect-id']
subscription_id = os.environ['subscription-id']
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)
timeout = 60
sender = '{}@appspot.gserviceaccount.com'.format(app_identity.get_application_id())

def send_approved_mail(message: pubsub_v1.subscriber.message.Message) -> None:
    mail.send_mail(sender=sender,
                   to="Albert Johnson <Albert.Johnson@example.com>",
                   subject="Your account has been approved",
                   body="""Your file is ready""")

                   

def main():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=send_approved_mail)
    print(f"Listening for messages on {subscription_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result() 
