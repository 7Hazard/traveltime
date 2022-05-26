import pyarrow.parquet as pq
import pandas as pd

__trips = pq.read_table('data/trips/yellow_tripdata_2019-01.parquet')
__trips: pd.DataFrame = __trips.to_pandas()
__trips = __trips[["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance", "PULocationID", "DOLocationID"]]

# remove all rows with trip distance of 0
__trips = __trips[__trips.trip_distance > 0.0]

# remove all rows with pickup time before 2019-01-01 00:00:00
__trips = __trips[__trips["tpep_pickup_datetime"] >= "2019-01-01 00:00:00"]

# remove all rows with pickup time after dropoff time
__trips = __trips[__trips["tpep_pickup_datetime"] <= __trips["tpep_dropoff_datetime"]]

# remove all rows with dropoff time before 2019-01-01 00:00:00
__trips = __trips[__trips["tpep_dropoff_datetime"] >= "2019-01-01 00:00:00"]

# add column with trip time in seconds
__trips["trip_time"] = (pd.to_datetime(__trips["tpep_dropoff_datetime"]) - pd.to_datetime(__trips["tpep_pickup_datetime"])).dt.total_seconds()

# print 10 random rows
# print(__trips.sample(10))

# plot [tpep_pickup_datetime, trip_distance, PUlocationID, and DOLocationID] vs trip_time
# trips.plot(x=["tpep_pickup_datetime", "trip_distance", "PULocationID", "DOLocationID"], y="trip_time", kind="scatter", figsize=(12, 6))
# plt.scatter(trips["tpep_pickup_datetime"], trips["trip_distance"], trips["PULocationID"], trips["DOLocationID"], c=trips["trip_time"], cmap="tab20")
