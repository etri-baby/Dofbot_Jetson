import paho.mqtt.client as mqtt
import threading
import base64
import time
import cv2

client = mqtt.Client(transport="websockets")

def on_connect(client, userdata, flags, rc):
    print("connect success")
    client.subscribe("my/topic")

def Camera_Handle():
    client.connect("129.254.174.120", 9002, 60)
    client.on_connect = on_connect
    
    client.loop_start()  # loop_forever() 대신 loop_start()로 변경

    

def camera(client):
    image = cv2.VideoCapture(0)
    image.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    image.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    try:
        
        while True:
            start = time.time()
            ret, frame = image.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_base64 = base64.b64encode(buffer).decode()
                client.publish("my/topic", jpg_base64, qos=0)
                end = time.time()
                t = end - start
                fps = 1/t
                print(fps)
                
    except KeyboardInterrupt:
        print("카메라 처리 종료")
        image.release()

def try_reconnect(client):
    while not client.is_connected():
        try:
            print("Trying to reconnect...")
            client.connect("129.254.174.120", 9002, 60)
            client.loop_start()
        except ConnectionError:
            print("Failed to reconnect. Retrying in 5 seconds...")
            time.sleep(5)

camera_thread = threading.Thread(target=Camera_Handle)
camera_thread.start()

try_reconnect(client)
camera(client)

