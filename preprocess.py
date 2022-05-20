import pyarrow.parquet as pq
import pandas as pd
import matplotlib.pyplot as plt

trips = pq.read_table('data/trips/yellow_tripdata_2019-01.parquet')
trips: pd.DataFrame = trips.to_pandas()
trips = trips[["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance", "PULocationID", "DOLocationID"]]

# remove all rows with trip distance of 0
trips = trips[trips.trip_distance > 0.0]

# remove all rows with pickup time before 2019-01-01 00:00:00
trips = trips[trips["tpep_pickup_datetime"] >= "2019-01-01 00:00:00"]

# remove all rows with pickup time after dropoff time
trips = trips[trips["tpep_pickup_datetime"] <= trips["tpep_dropoff_datetime"]]

# remove all rows with dropoff time before 2019-01-01 00:00:00
trips = trips[trips["tpep_dropoff_datetime"] >= "2019-01-01 00:00:00"]

# add column with trip time in seconds
trips["trip_time"] = (pd.to_datetime(trips["tpep_dropoff_datetime"]) - pd.to_datetime(trips["tpep_pickup_datetime"])).dt.total_seconds()

# print 10 random rows
print(trips.sample(10))

# plot [tpep_pickup_datetime, trip_distance, PUlocationID, and DOLocationID] vs trip_time
# trips.plot(x=["tpep_pickup_datetime", "trip_distance", "PULocationID", "DOLocationID"], y="trip_time", kind="scatter", figsize=(12, 6))
# plt.scatter(trips["tpep_pickup_datetime"], trips["trip_distance"], trips["PULocationID"], trips["DOLocationID"], c=trips["trip_time"], cmap="tab20")

# read all taxi zones from csv file
taxi_zones = pd.read_csv("data/zones/taxi_zone_lookup.csv")

# print 10 random rows from taxi_zones
# print(taxi_zones.sample(10))

