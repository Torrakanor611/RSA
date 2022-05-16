import paho.mqtt.client as mqtt
import json

client = mqtt.Client()

client.connect("192.168.98.20" , 1883, 60)

f = open('data.json')
data = json.load(f)

client.publish("vanetza/in/cam", json.dumps(data))

client.disconnect()