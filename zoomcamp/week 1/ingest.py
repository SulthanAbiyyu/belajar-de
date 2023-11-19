import os
import logging
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

def main():
    username = os.getenv('DATABASE_USERNAME')
    password = os.getenv('DATABASE_PASSWORD')
    host = os.getenv('DATABASE_HOST')
    port = os.getenv('DATABASE_PORT')
    database = os.getenv('DATABASE_NAME')
    table_name = os.getenv('TABLE_NAME')
    url = os.getenv('URL')
    
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
        logging.info(f"Uploaded chunk {i}")
    
    logging.info("Cleaning up")
    os.remove("output.parquet")
    os.remove("output.csv")

if __name__ == "__main__":            
    main()


