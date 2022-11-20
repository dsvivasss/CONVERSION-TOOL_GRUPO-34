import json
import ffmpeg
import requests
from google.cloud import pubsub_v1, storage
from environments import project_id, file_topic_name, upload_bucket_name, download_bucket_name


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, file_topic_name)
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
    path_name = file_data.get('pathName')
    blob = upload_bucket.blob(path_name)
    blob.download_to_filename(path_name)
    print('Donwload local ok...')
    convert_name = f'{path_name}_convert'
    ffmpeg.input(path_name).output(convert_name, format=file_data.get('newFormat')).overwrite_output().run()
    blob = download_bucket.blob(new_name)
    blob.upload_from_filename(path_name)
    print('Upload convert ok...')
    os.remove(path_name)
    os.remove(convert_name)

    url = f'{host}/api/file/{file_data.get("id")}'
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