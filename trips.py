import pyarrow.parquet as pq
import pandas as pd

def readAndCleanData(filename, yellow=True):
    pickupTime = "tpep_pickup_datetime" if yellow else "lpep_pickup_datetime"
    dropoffTime = "lpep_dropoff_datetime" if yellow else "lpep_dropoff_datetime"

    __trips = pq.read_table(filename)
    __trips: pd.DataFrame = __trips.to_pandas()
    __trips = __trips[[pickupTime, dropoffTime, "trip_distance", "PULocationID", "DOLocationID"]]

    # remove all rows with trip distance of 0
    __trips = __trips[__trips.trip_distance > 0.0]

    # remove all rows with pickup time before 2019-01-01 00:00:00
    __trips = __trips[__trips[pickupTime] >= "2019-01-01 00:00:00"]

    # remove all rows with pickup time after dropoff time
    __trips = __trips[__trips[pickupTime] <= __trips[dropoffTime]]

    # remove all rows with dropoff time before 2019-01-01 00:00:00
    __trips = __trips[__trips[dropoffTime] >= "2019-01-01 00:00:00"]

    # add column with trip time in seconds
    __trips["trip_time"] = (pd.to_datetime(__trips[dropoffTime]) - pd.to_datetime(__trips[pickupTime])).dt.total_seconds()

    # remove dropoff time column
    __trips = __trips.drop(columns=[dropoffTime])

    # change pickupTime year to start of epoch year
    __trips[pickupTime] = __trips[pickupTime].apply(lambda x: x.replace(year=1970))

    # convert pickupTime to numeric values
    __trips[pickupTime] = pd.to_numeric(__trips[pickupTime])

    # plot pickupTime trip_distance, PUlocationID, and DOLocationID] vs trip_time
    # trips.plot(x=[pickupTime, "trip_distance", "PULocationID", "DOLocationID"], y="trip_time", kind="scatter", figsize=(12, 6))
    # plt.scatter(trips[pickupTime], trips["trip_distance"], trips["PULocationID"], trips["DOLocationID"], c=trips["trip_time"], cmap="tab20")

    # get [pickupTime, "trip_distance", "PULocationID", "DOLocationID"] from trips as X values
    x = __trips[[pickupTime, "trip_distance", "PULocationID", "DOLocationID"]].to_numpy()

    # get ["trip_time"] from trips as y values
    y = __trips[["trip_time"]].to_numpy().ravel()

    return __trips, x, y

trips, x, y = readAndCleanData("data/trips/green_tripdata_2019-01.parquet", False)
# trips, x, y = readAndCleanData("data/trips/yellow_tripdata_2019-01.parquet")
print(f"Trip data: \n{trips}\n")
print(f"X values: \n{x}\n")
print(f"Y values: \n{y}\n")
