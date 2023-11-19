import os
import logging
import argparse
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

def main(params):
    username = params.username
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table_name = params.table_name
    url = params.url
    
    logging.info("Downloading data")
    os.system(f"wget {url} -O output.parquet")

    logging.info("Converting to csv")
    pq_df = pd.read_parquet("output.parquet")
    pq_df.to_csv("output.csv", index=False)
    
    logging.info("Uploading to database")
    engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")
    df_iter = pd.read_csv("output.csv", iterator=True, chunksize=100_000)

    i = 0
    while True:
        try:
            df = next(df_iter)
        except StopIteration:
            break
        
        df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
        df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
        
        if i == 0:
            df.head(0).to_sql(table_name, con=engine, if_exists="replace", index=False)
            i += 1
        else:
            df.to_sql(table_name, con=engine, if_exists="append", index=False)
            i += 1
        print("Chunk", i)
    
    logging.info("Cleaning up")
    os.remove("output.parquet")
    os.remove("output.csv")

if __name__ == "__main__":            
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)
    parser.add_argument("--host", type=str)
    parser.add_argument("--port", type=str)
    parser.add_argument("--database", type=str)
    parser.add_argument("--table_name", type=str)
    parser.add_argument("--url", type=str, default="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet")
    parser.add_argument("--parquet", type=bool, default=True)
    params = parser.parse_args()

    main(params)


