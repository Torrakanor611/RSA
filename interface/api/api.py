import paho.mqtt.client as mqtt
import time
from flask import Flask
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# take environment variables from .env
load_dotenv()

# InfluxDB config
BUCKET = os.getenv('INFLUXDB_BUCKET')
influx_cli = InfluxDBClient(url=os.getenv('INFLUXDB_URL'), token=os.getenv('INFLUXDB_TOKEN'), org=os.getenv('INFLUXDB_ORG'))
query_api = influx_cli.query_api()

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/api/getLocations')
async def get_locations() -> dict:
    query = f'''from(bucket:"{os.getenv('INFLUXDB_BUCKET')}")\
    |> range(start: -1s)\
    |> filter(fn:(r) => r._measurement == "cam")\
    |> filter(fn:(r) => r.stationID == "1" or r.stationID == "2" or r.stationID == "3" or r.stationID == "4")
    |> sort(columns: ["_time"])
    |> limit(n: 4)
    '''
    result = query_api.query(org=os.getenv('INFLUXDB_ORG'), query=query)

    # print(result)

    last_entrys = [None] * 4
    for table in result:
        for record in table.records:
            values = record.values
            last_entrys[int(values.get('stationID')) - 1] = (record.get_value(), values.get('_time'))

    data = []
    print(last_entrys)
    for i in range(4):
        aux = last_entrys[i]
        aux1 = aux[0].split('&')
        data.append({'stationID': i, 'lat': float(aux1[0]), 'lng': float(aux1[1])})

    return json.dumps(data)

app.run()