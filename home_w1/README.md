## Question 1. Understanding Docker Images

Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What's the version of `pip` in the image?
~~~
docker run --rm -it python:3.13 bash
pip --version
~~~

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?
~~~
docker compose up
~~~

## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

~~~
SELECT COUNT(*)
FROM public.green_taxi_data
WHERE lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01'
  AND trip_distance <= 1.0000
~~~

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

~~~
SELECT lpep_pickup_datetime::date AS pickup_date,
       ROUND(CAST(SUM(trip_distance) AS numeric),2) AS total_dist
FROM public.green_taxi_data
WHERE trip_distance < 100.0000
GROUP BY lpep_pickup_datetime::date
ORDER BY ROUND(CAST(SUM(trip_distance) AS numeric),2) DESC
LIMIT 1
~~~

## Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

~~~
SELECT "PULocationID",
       "Zone",
       SUM(total_amount) AS total
FROM public.green_taxi_data
LEFT JOIN public.taxi_zone_lookup
ON "PULocationID" = "LocationID"
WHERE lpep_pickup_datetime::date = '2025-11-18'
GROUP BY "PULocationID","Zone"
ORDER BY SUM(total_amount) DESC
LIMIT 1
~~~





