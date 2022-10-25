import logging
import json
import ffmpeg
import requests
from kafka import KafkaConsumer
import pathlib



def main():
    try:
        print(pathlib.Path(__file__).parent.resolve())
        # To consume latest messages and auto-commit offsets
        host = 'http://api:5001'
        consumer = KafkaConsumer('convert_song',auto_offset_reset='earliest',bootstrap_servers='kafka:29092')
        print('Kafka Consumer has been initiated...')
        for msg in consumer:
            print('Start ...')
            file_data = json.loads(msg.value)
            name = file_data.get('fileName').split('.')
            new_name= name[0] + '.'+ file_data.get('newFormat')
            ffmpeg.input('/convert/app/uploads/'+file_data.get('fileName')).output('/convert/app/process/'+new_name, format=file_data.get('newFormat')).overwrite_output().run()
            print('Convert ok...')
            url = f'{host}/api/file/{file_data.get("id")}'
            print(url)
            response = requests.put(url)
            print(f'Update status ok...{response.status_code}')
    except Exception as e:
        logging.info('Connection successful', e)