from getpass import getpass
from utils import MinioBasicOperator

import os
import glob
import json
import pandas as pd


endpoint = getpass(prompt='endpoint: ')
access_key = getpass(prompt='access_key: ')
secret_key = getpass(prompt='secret_key: ')

client = MinioBasicOperator(
    endpoint=endpoint,
    access_key=access_key,
    secret_key=secret_key,
    bucket_name="stock-price-kafka-biyu"
)

os.mkdir("data")

data_path = client.ls_dir("stock/")[1:]
for path in data_path:
    client.get_file(path, f"data/{path.split('/')[-1]}")

local_data = glob.glob("data/*.json")

data = []
for i in local_data:
    with open(i, "r") as f:
        data.append(json.load(f))

os.mkdir("data/transformed")

df = pd.DataFrame(data)
df.to_csv("./data/transformed/stock.csv", index=False)