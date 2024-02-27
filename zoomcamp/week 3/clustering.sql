CREATE OR REPLACE TABLE `taxi-rides-ny-413704.ny_taxi.yellow_cabdata_clustered`
PARTITION BY
  DATE(tpep_pickup_datetime) 
CLUSTER BY
  vendorid AS
SELECT * FROM `taxi-rides-ny-413704.ny_taxi.yellow_cab_data`;

SELECT COUNT(*) AS trips
FROM `taxi-rides-ny-413704.ny_taxi.yellow_cabdata_clustered`
WHERE vendorid=1;
