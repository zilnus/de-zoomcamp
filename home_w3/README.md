## Question 1

What is count of records for the 2024 Yellow Taxi Data?

~~~
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `kestra-demo-486215.bq_hw3.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_hw3_2026_satria/yellow_tripdata_2024-*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE `kestra-demo-486215.bq_hw3.yellow_tripdata_2024_non_partition` AS
SELECT * FROM `kestra-demo-486215.bq_hw3.external_yellow_tripdata_2024`;

SELECT COUNT(*) FROM `kestra-demo-486215.bq_hw3.external_yellow_tripdata_2024`
~~~

## Question 2

Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

~~~
SELECT COUNT(DISTINCT(PULocationID)) FROM `kestra-demo-486215.bq_hw3.external_yellow_tripdata_2024`;

SELECT COUNT(DISTINCT(PULocationID)) FROM `kestra-demo-486215.bq_hw3.yellow_tripdata_2024_non_partition`;
~~~

## Question 4

How many records have a fare_amount of 0?

~~~
SELECT COUNT(*) 
FROM `kestra-demo-486215.bq_hw3.yellow_tripdata_2024_non_partition`
WHERE fare_amount = 0;
~~~

## Question 5

What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

~~~
CREATE OR REPLACE TABLE `kestra-demo-486215.bq_hw3.yellow_tripdata_2024_partition`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS (
  SELECT * FROM `kestra-demo-486215.bq_hw3.external_yellow_tripdata_2024`
);
~~~

## Question 6

Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

~~~
SELECT COUNT(DISTINCT(VendorID))
FROM `kestra-demo-486215.bq_hw3.yellow_tripdata_2024_non_partition`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15'

SELECT COUNT(DISTINCT(VendorID))
FROM `kestra-demo-486215.bq_hw3.yellow_tripdata_2024_partition`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15'
~~~

## Question 9

Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

~~~
SELECT COUNT(*)
FROM `kestra-demo-486215.bq_hw3.yellow_tripdata_2024_non_partition`
~~~



