# Week 1: Introduction and Prerequisites

dataset: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

postgre database

```bash
docker run -it ^
    -e POSTGRES_USER="root" ^
    -e POSTGRES_PASSWORD="root" ^
    -e POSTGRES_DB="ny_taxi" ^
    -v "d:\code\project\road to data science\exercise\36. data engineering\zoomcamp\week 1\ny_taxi_data:/var/lib/postgresql/data" ^
    -p 5432:5432 ^
    --network=pg-network ^
    --name=pg-db ^
    postgres:13
```

postgre pgAdmin

```bash
docker run -it ^
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" ^
    -e PGADMIN_DEFAULT_PASSWORD="root" ^
    -p 8080:80 ^
    --network=pg-network ^
    --name=pg-admin ^
    dpage/pgadmin4
```

Dockerfile for data ingestion

```Dockerfile
FROM python:3.10

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 pyarrow fastparquet

WORKDIR /app

COPY ingest.py ingest.py

ENTRYPOINT [ "python", "ingest.py" ]
```

build the dockerfile

```bash
docker build -t taxi-ingest:latest .
```

run ingestion for taxi trip records

```
docker run -it ^
    taxi-ingest:latest ^
        --username=root ^
        --password=root ^
        --host=pgdb ^
        --port=5432 ^
        --database=ny_taxi ^
        --table_name=trips
```

using docker compose

ingest data

```
docker-compose -f docker-compose-build up -d
```

run server and pgAdmin

```
docker-compose -f docker-compose-server up -d
```
