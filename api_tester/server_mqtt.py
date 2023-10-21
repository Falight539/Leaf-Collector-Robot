import paho.mqtt.client as paho
from paho import mqtt

import json
import base64

import numpy as np
import cv2

from TerrainAnalysis import path_planer

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.username_pw_set('OMEN15', '53663_Icanfly')
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.connect("1cd8a66a6ff341b2a118559d849c2e30.s2.eu.hivemq.cloud", 8883)

client.subscribe('img/txt', 1)

def on_message(client, userdata, msg):
    print("I'm in")
    image_array = np.frombuffer(base64.b64decode(msg.payload), dtype=np.uint8)
    print(image_array)
    cv2.imshow("test", image_array)

client.on_message = on_message
client.loop_forever()