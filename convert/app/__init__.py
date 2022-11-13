import logging
import json
import ffmpeg
import requests
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from google.cloud import storage
from datetime import datetime

host= os.environ['api-host']
project_id = os.environ['proyect-id']
subscription_id = os.environ['subscription-id']
upload_bucket_name= os.environ['upload-bucket-name']
download_bucket_name= os.environ['download-bucket-name']
#host= 'http://35.245.77.88:5001'
#project_id = 'convertor-tool'
#subscription_id = 'convert_song_sub'
#upload_bucket_name= 'original-song'
#download_bucket_name= 'convert-song'
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)
timeout = 60

storage_client = storage.Client()
upload_bucket = storage_client.bucket(upload_bucket_name)
download_bucket = storage_client.bucket(download_bucket_name)

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def callback(message: pubsub_v1.subscriber.message.Message) -> None:

    file_data = json.loads(message.data)
    name = file_data.get('fileName').split('.')
    new_name= name[0] + '.'+ file_data.get('newFormat')
    blob = upload_bucket.blob(file_data.get('fileName'))
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    temp_ori = file_data.get('fileName')
    blob.download_to_filename(f'{timestamp}_{temp_ori}')
    print('Donwload local ok...')
    now = datetime.now()
    timestamp2 = datetime.timestamp(now)
    ffmpeg.input(f'{timestamp}_{temp_ori}').output(f'{timestamp2}_{new_name}', format=file_data.get('newFormat')).overwrite_output().run()
    blob = download_bucket.blob(new_name)
    blob.upload_from_filename(f'{timestamp2}_{new_name}')
    print('Upload convert ok...')
    
    os.remove(f'{timestamp}_{temp_ori}')
    os.remove(f'{timestamp2}_{new_name}')

    url = f'{host}/api/file/{file_data.get("id")}'
    print(url)
    response = requests.put(url)
    print(f'Update status ok...{response.status_code}')

    message.ack()
    

def main():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result() 