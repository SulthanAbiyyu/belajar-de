-- Create partitioned data by date
CREATE OR REPLACE TABLE `taxi-rides-ny-413704.ny_taxi.yellow_cabdata_partitioned`
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM `taxi-rides-ny-413704.ny_taxi.yellow_cab_data`;

-- Impact of partition
SELECT DISTINCT(vendorid)
FROM `taxi-rides-ny-413704.ny_taxi.yellow_cabdata_non_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-01-30';

SELECT DISTINCT(vendorid)
FROM `taxi-rides-ny-413704.ny_taxi.yellow_cabdata_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-01-30';

-- Inspect the partition
SELECT table_name, partition_id, total_rows
FROM `ny_taxi.INFORMATION_SCHEMA_PARTITIONS`
WHERE table_name = `yellow_cabdata_partitioned`
ORDER BY total_rows DESC