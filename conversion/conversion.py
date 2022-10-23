import requests
from kafka import KafkaConsumer, KafkaProducer
import json

host = 'http://127.0.0.1:5000'

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer,
    # partitioner=get_partition
    )

if __name__ == '__main__':
    url = f'{host}/api/auth/login/'

    r = requests.post(
        url,
        headers={
            "Content-Type": "application/json"
        },
        json={
            "username": "conversion",
            "password": "nacional"
        })

    url = f'{host}/api/tasks/'

    tasks = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {r.json()['token']}"
        },
    )

    consumer = KafkaConsumer(
        'conversion',
        bootstrap_servers=['localhost:9092'],
        # earliest means that the consumer will read from the beginning of the topic
        auto_offset_reset='earliest',
        group_id='consumer-group-a'
    )

    print('Waiting for messages...')
    for message in consumer:
        
        # Cron, each n seconds

        # Convert file
        
        # HTTP request to update the task to the API
        
        print('Received message: {}'.format(message.value))
        
        
        