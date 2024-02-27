-- Create external table (the data source is not in BQ)
CREATE OR REPLACE EXTERNAL TABLE `taxi-rides-ny-413704.ny_taxi.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['']
);

SELECT *
FROM `taxi-rides-ny-413704.ny_taxi.external_yellow_tripdata`
LIMIT 10;

-- Create non partitioned data
CREATE OR REPLACE TABLE `taxi-rides-ny-413704.ny_taxi.yellow_cabdata_non_partitioned` AS 
SELECT * FROM `taxi-rides-ny-413704.ny_taxi.external_yellow_tripdata`;