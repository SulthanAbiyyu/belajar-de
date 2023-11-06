from kafka import KafkaConsumer
from time import sleep
from json import dumps,loads
from getpass import getpass
from utils import MinioBasicOperator

endpoint = getpass(prompt='endpoint: ')
access_key = getpass(prompt='access_key: ')
secret_key = getpass(prompt='secret_key: ')

client = MinioBasicOperator(
    endpoint=endpoint,
    access_key=access_key,
    secret_key=secret_key,
    bucket_name="stock-price-kafka-biyu"
)

consumer = KafkaConsumer(
    'stock_price',
     bootstrap_servers=['127.0.0.1:9092'],
    value_deserializer=lambda x: loads(x.decode('utf-8')))

for i, c in enumerate(consumer):
    client.upload_json(c.value, f"stock/stock_price_{i}.json")