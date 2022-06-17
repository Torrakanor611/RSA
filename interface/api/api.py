import paho.mqtt.client as mqtt
import time
from flask import Flask

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):
    print('received')

cli = mqtt.Client("id")
cli.connect("192.168.98.50", 1883, 60)
time.sleep(1)
cli.on_message = on_message
cli.on_connect = on_connect
cli.subscribe('vanetza/out/cam')

# while True:
#     cli.loop()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

app.run()
cli.loop_forever()