import paho.mqtt.client as paho
from paho import mqtt
import base64
import json
import time

import cv2
import numpy as np

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.username_pw_set('Robot', '53663_Icanfly')
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.connect("1cd8a66a6ff341b2a118559d849c2e30.s2.eu.hivemq.cloud", 8883)

img = cv2.cvtColor(cv2.imread(r'./BuildModel/img/dataset/14.png'), cv2.COLOR_BGR2RGB)
img = np.array(cv2.resize(img, (256, 256)), dtype=np.uint8)

encoded = base64.b64encode(img)

encoded_image_data = base64.b64encode(encoded)

client.publish('img/txt', encoded_image_data, 1)

client.disconnect()

# *How to encode image as base64*

# with open("image.jpg", "rb") as f:
#     image_data = f.read()
# 
# encoded_image_data = base64.b64encode(image_data)