from concurrent.futures import thread
import paho.mqtt.client as mqtt
from threading import Thread
from queue import Queue
import json
import time
import os

def update_cam(cam, update):
    for key in update.keys():
        if key in cam.keys():
            cam[key] = update[key]
        else:
            print('update CAM with bad configuration!')

    return cam

def on_message(client, userdata, message):
    print('------>obu5 received message on topic ',str(message.topic))
    # print('obu5 received message:',str(message.payload.decode("utf-8")))
    # print('\n\n')
    pass

def launch_obu(data):
    client = mqtt.Client(client_id=f'_{data[0]}')
    client.connect(data[0]['ip'], 1883, 60)
    if data[0]['ip'] == '192.168.98.50':
        client.on_message = on_message
    cam = data[1]
    client.publish('vanetza/in/cam', json.dumps(cam))
    client.subscribe('vanetza/out/denm')
    client.subscribe('vanetza/out/cam')
    count = 0.5

    while True:
    ## update cam
        if str(count) in data[2].keys():
            cam = update_cam(cam, data[2][str(count)])
        client.publish('vanetza/in/cam', json.dumps(cam))


        if len(data) == 5:
            if str(count) in data[4].keys():
                client.publish('vanetza/in/denm', json.dumps(data[3]))

        count += 0.5
        # time.sleep(0.5)
        client.loop(0.5) #check for messages

    time.sleep(2) # wait
    client.disconnect()

def main():
    files = os.listdir('obu')
    files = [f.split('.')[0] for f in files]

    threads = [Thread(target=launch_obu, name=f'_{obu}', args=(json.load(open(f'obu/{obu}.json')),  )) for obu in files]

    ## start the threads
    print(f'threads started!\n')
    [t.start() for t in threads]

    ## stop the threads
    [t.join() for t in threads]
    print(f'threads finished!\n')

    return 0

if __name__ == "__main__":
    main()