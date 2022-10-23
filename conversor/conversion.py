from urllib import request
from kafka import KafkaConsumer, KafkaProducer
import json
import ffmpeg
import requests

host = 'http://localhost:5000'

consumer = KafkaConsumer('convert_song', bootstrap_servers='localhost:9092', fetch_max_wait_ms = 10000)
print('Kafka Consumer has been initiated...')

if __name__ == '__main__':
    for msg in consumer:
        print('Start ...')
        file_data = json.loads(msg.value)
        name = file_data.get('fileName').split('.')
        newName= name[0] + '.'+ file_data.get('newFormat')
        ffmpeg.input('./uploads/'+file_data.get('fileName')).output('./process/'+newName, format=file_data.get('newFormat')).overwrite_output().run()
        print('Convert ok...')
        url = f'{host}/api/file/{file_data.get("id")}'
        print(url)
        response = requests.put(url)
        print(f'Update status ok...{response.status_code}')