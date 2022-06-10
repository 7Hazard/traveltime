import json
import pickle
from datetime import datetime
from flask import Flask, request
from pandas import DataFrame
from sklearn import neural_network
from zones import latlonToZoneId
import requests

# load model.pkl
model: neural_network.MLPRegressor = pickle.load(open("model.pkl", 'rb'))

app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def predict():
    # get fromlat, tolat, fromlong, tolong from query params
    fromlon = float(request.args.get("fromlon"))
    fromlat = float(request.args.get("fromlat"))
    tolon = float(request.args.get("tolon"))
    tolat = float(request.args.get("tolat"))

    # get zone from lat, lon
    fromzone = latlonToZoneId(fromlon, fromlat)
    tozone = latlonToZoneId(tolon, tolat)

    # check if zones are valid
    if fromzone is None or tozone is None:
        return "Invalid zones"

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }
    req = requests.get(f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248327dfbd785f541cfa1c6314bcbeb3cd3&start={fromlon},{fromlat}&end={tolon},{tolat}", headers=headers)
    j = json.loads(req.text)
    features = j['features'][0]
    summary = features['properties']['summary']
    distanceMeters = summary["distance"]
    distanceMiles = distanceMeters*0.0006213712

    # get time as datetime from query params
    time = request.args.get("time")
    # convert time to datetime object from 2019-01-01T00:00:00.000Z format
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    # get month, day and time of day in seconds from time
    month = time.month
    day = time.day
    time_of_day = time.hour*3600 + time.minute*60 + time.second

    # predict travel time from model
    x = DataFrame([{
        "pickup_month": month,
        "pickup_day": day,
        "pickup_time": time_of_day,
        "trip_distance": distanceMiles,
        "PULocationID": fromzone,
        "DOLocationID": tozone,
    }])
    # print(x)
    travel_time = model.predict(x)

    return f"{travel_time[0]}"

# example request
# http://localhost:5000/predict?fromlon=-74.012878&fromlat=40.702417&tolon=-73.985758&tolat=40.748094&time=2019-03-15T13:37:54.000Z
