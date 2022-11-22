import os
import json
import ffmpeg
import requests
from google.cloud import pubsub_v1, storage


project_id = os.getenv('project-id', None)
if project_id is None:
    project_id='conversiontoolg34'
    api_host= 'http://35.245.77.88:5001'
    file_sub_name = 'email-topic-sub'
    download_bucket_name='convert-song-v1'
    upload_bucket_name='original-song-v1'
else:
    api_host = os.getenv('api-host', None)
    file_sub_name = os.getenv('file-sub-name', None)
    upload_bucket_name= os.getenv('upload-bucket-name', None)
    download_bucket_name= os.getenv('download-bucket-name', None)


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, file_sub_name)
timeout = 3600

storage_client = storage.Client()
upload_bucket = storage_client.bucket(upload_bucket_name)
download_bucket = storage_client.bucket(download_bucket_name)

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def callback(message: pubsub_v1.subscriber.message.Message) -> None:

    file_data = json.loads(message.data)
    name = file_data.get('fileName').split('.')
    path_name = file_data.get('pathName')
    blob = upload_bucket.blob(path_name)
    blob.download_to_filename(path_name)
    print('Donwload local ok...')
    convert_name = f'{path_name}_convert'
    ffmpeg.input(path_name).output(convert_name, format=file_data.get('newFormat')).overwrite_output().run()
    timestamp = file_data.get('pathName').split('_')[0]
    new_name= name[0] + '.'+ file_data.get('newFormat')
    new_path = f'{timestamp}_{new_name}'
    blob = download_bucket.blob(new_path)
    blob.upload_from_filename(convert_name)
    print('Upload convert ok...')
    os.remove(path_name)
    os.remove(convert_name)

    url = f'{api_host}/api/file/{file_data.get("id")}'
    print(url)
    response = requests.put(url)
    print(f'Update status ok...{response.status_code}')

    message.ack()
    

if __name__ == '__main__':
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result() 