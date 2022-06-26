from concurrent.futures import thread
import paho.mqtt.client as mqtt
from threading import Thread
from queue import Queue
import json
import time
import os
import numpy as np
import cv2
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
from threading import current_thread

# take environment variables from .env
load_dotenv()

# InfluxDB config
BUCKET = os.getenv('INFLUXDB_BUCKET')
influx_cli = InfluxDBClient(url=os.getenv('INFLUXDB_URL'), token=os.getenv('INFLUXDB_TOKEN'), org=os.getenv('INFLUXDB_ORG'))
write_api = influx_cli.write_api()

def update_cam(cam, update):
    for key in update.keys():
        if key in cam.keys():
            cam[key] = update[key]
        else:
            print('update CAM with bad configuration!')

    return cam

def on_message(client, userdata, message):
    msg_payload = json.loads(str(message.payload.decode("utf-8")))
    # if topic is 'vanetza/out/cam'
    if message.topic == 'vanetza/out/cam':
        lat = msg_payload['latitude']
        lng = msg_payload['longitude']
        # payload to send
        data = Point('cam').tag('stationID', msg_payload['stationID']).field('lat&lng', f'{lat}&{lng}')
        # send to influxDB
        write_api.write(bucket=BUCKET, record=data)

    # if topic is 'vanetza/out/denm'
    if message.topic == 'vanetza/out/denm':
        # lat = msg_payload['fields']['denm']['management']['eventPosition']['latitude']
        # lng = msg_payload['fields']['denm']['management']['eventPosition']['longitude']
        cause = msg_payload['fields']['denm']['situation']['eventType']['causeCode']
        subcause = msg_payload['fields']['denm']['situation']['eventType']['subCauseCode']
        # payload to send
        data = Point('denm').field('cause', f'{cause}').field('subcause', f'{subcause}')
        # send to influxDB
        write_api.write(bucket=BUCKET, record=data)
        print(f'sended to influx, {cause}, {subcause}!')

def on_connect(client, userdata, flags, rc):
    thread = current_thread()
    if rc==0:
        print(f'thread {thread.name} connected OK, returned code={rc}')
    else:
        print(f' thread {thread.name} Bad connection, returned code={rc}')

def on_disconnect(client, userdata, rc):
    thread = current_thread()
    if rc==0:
        print(f'thread {thread.name} disconnected, returned code={rc}')
    else:
        print(f' thread {thread.name} disconnected, returned code={rc}')
 
def launch_obu(data):
    client = mqtt.Client(client_id=f'_{data[0]}')
    client.connect(data[0]['ip'], 1883, 30)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    time.sleep(1)
    cam = data[1]
    if data[0]['ip'] == '192.168.98.50':
        client.on_message = on_message
    client.publish('vanetza/in/cam', json.dumps(cam))
    client.subscribe('vanetza/out/denm')
    client.subscribe('vanetza/out/cam')
    count = 0.0

    client.loop_start()

    while True:
        ## update cam
        if str(count) in data[2].keys():
            cam = update_cam(cam, data[2][str(count)])
        client.publish('vanetza/in/cam', json.dumps(cam))

        if len(data) == 5:
            if str(count) in data[4].keys():
                client.publish('vanetza/in/denm', json.dumps(data[3]))

        count += 0.5
        time.sleep(0.5)

    client.loop_stop()
    time.sleep(2) # wait
    client.disconnect()

def video_stream(capture):
    # Check if camera opened successfully
    if (capture.isOpened() == False):
        print("Error opening video stream or file")
        exit(1)

    while(capture.isOpened()):
        ret, frame = capture.read()
        if ret == True:
            cv2.imshow('Video', frame)
            # Press 'q' to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    capture.release()
    cv2.destroyAllWindows()

def main():
    files = os.listdir('obu')
    files = [f.split('.')[0] for f in files]

    threads = [Thread(target=launch_obu, name=f'_{obu}', args=(json.load(open(f'obu/{obu}.json')),  )) for obu in files]
    threads.append( Thread(target=video_stream, name=f'video_stream', args=(cv2.VideoCapture('video/vid1.mp4'), ) ))

    ## start the threads
    print(f'threads started!\n')
    [t.start() for t in threads]

    ## stop the threads
    [t.join() for t in threads]
    print(f'threads finished!\n')

    return 0

if __name__ == "__main__":
    main()