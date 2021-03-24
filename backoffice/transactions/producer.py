from kafka import KafkaProducer
from json import dumps


def send_transaction(str_data):
    producer = KafkaProducer(bootstrap_servers=['kafka_broker:29092'], value_serializer = lambda x: dumps(x).encode('utf-8'))
    producer.send('transaction_record', value=str_data)