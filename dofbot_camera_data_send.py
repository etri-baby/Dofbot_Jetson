import paho.mqtt.client as mqtt
import threading
import cv2
import json
from Arm_Lib import Arm_Device

def on_connect(client, userdata, flags, rc):
    print("연결 성공, 결과 코드: " + str(rc))
    client.subscribe("my/topic")

def on_message(client, userdata, msg):
    try:
        print(msg.payload)
    except:
        print("not decoding message.....")

def Camera_Handle():
    client = mqtt.Client(transport="websockets")
    client.connect("129.254.174.120", 9002, 60)
    print("connected")
    client.on_connect = on_connect
    client.on_message = on_message
    print("message arrived")
    client.loop_forever()

    camera(client)

camera_thread = threading.Thread(target=Camera_Handle)
camera_thread.start()

def camera(client):
    image = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = image.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                client.publish("my/topic", buffer.tobytes(), qos=1)
    except KeyboardInterrupt:
        print("카메라 처리 종료")
        image.release()
