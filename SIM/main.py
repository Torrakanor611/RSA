import paho.mqtt.client as mqtt
from threading import Thread
import json
import time
import os


def launch_obu(data):
    client = mqtt.Client()
    client.connect(data[0]['ip'], 1883, 60)
    client.publish("vanetza/in/cam", json.dumps(data[1]))

    while True:
        
        ## update cam info with data[3] dict



        time.sleep(0.5)

    client.disconnect()

def main():
    files = os.listdir('obu')
    files = [f.split('.')[0] for f in files]

    threads = [Thread(target=launch_obu, name=f'_{obu}', args=(json.load(open(f'obu/{obu}.json')), )) for obu in files]

    # start the threads
    for thread in threads:
        print(f'thread: {thread.name} started!\n')
        thread.start()

    # wait for the threads to complete
    for thread in threads:
        thread.join()
        print(f'thread: {thread.name} finished!\n')

    return 0

if __name__ == "__main__":
    main()