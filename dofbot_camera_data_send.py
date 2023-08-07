import paho.mqtt.client as mqtt
import threading
import base64
import time
import cv2

client2 = mqtt.Client(transport="websockets")

def on_connect_socket(client2, userdata, flags, rc):
    if(rc == 0):
        print("Connected to MQTT broker")
        client2.subscribe("jetson/camera")
    else:
        print("Failed to connect, code: ", rc)


def Camera_Handle():
    client2.connect("129.254.174.120", 9002, 60)
    client2.on_connect = on_connect_socket
    if(client2.on_connect_fail):
        try_reconnect(client2)
    else:
        camera(client2)
    
    client2.loop_start()  # loop_forever()

def camera(client2):
    image = cv2.VideoCapture(0)
    image.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    image.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    try:
        
        while True:
            ret, frame = image.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_base64 = base64.b64encode(buffer).decode()
                client2.publish("jetson/camera", jpg_base64, qos=0)
                
    except KeyboardInterrupt:
        print("카메라 처리 종료")
        image.release()

def try_reconnect(client2):
    while not client2.is_connected():
        try:
            print("Trying to reconnect...")
            client2.connect("129.254.174.120", 9002, 60)
            client2.loop_start()
        except ConnectionError:
            print("Failed to reconnect. Retrying in 3 seconds...")
            time.sleep(3)

camera_thread = threading.Thread(target=Camera_Handle)
camera_thread.start()

try_reconnect(client2)

