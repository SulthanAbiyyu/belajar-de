from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from time import sleep
from json import dumps
import pandas as pd

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092", 
    client_id='test'
)

topic_list = []
topic_list.append(NewTopic(name="stock_price", num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)

producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'], #change ip here
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
df = pd.read_csv("https://raw.githubusercontent.com/darshilparmar/stock-market-kafka-data-engineering-project/main/indexProcessed.csv")
while True:
    dict_stock = df.sample(1).to_dict(orient='records')[0]
    producer.send('stock_price', value=dict_stock)
    sleep(1)