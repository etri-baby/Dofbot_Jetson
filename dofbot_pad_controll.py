import paho.mqtt.client as mqtt
import threading
import json
import time
import cv2
import base64
from Arm_Lib import Arm_Device

# 게임패드 데이터를 저장할 변수 선언
gamepad_data = None

def on_connect(client, userdata, flags, rc):
    print("연결 성공, 결과 코드: " + str(rc))
    # 게임패드 데이터를 topic 구독
    client.subscribe("my/topic")

def on_connect_socket(client, userdata, flags, rc):
    print("socket 연결 성공, 결과 코드: " + str(rc))
    # 게임패드 데이터를 topic 구독
    client.subscribe("jetson/camera")


def on_message(client, userdata, msg):
    global gamepad_data
    # 수신된 메시지 파싱
    
    try:
        payload = msg.payload.decode()
        gamepad_data = json.loads(payload)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

def publish_camera_data(client, camera_data):
    client.publish("jetson/camera", camera_data, qos=1)

def handle_camera():
    image = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = image.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_base64 = base64.b64encode(buffer).decode()
                publish_camera_data(client2, jpg_base64)
    except KeyboardInterrupt:
        print("카메라 처리 종료")
        image.release()

def handle_gamepad():
    Arm = Arm_Device()
    s_time = 500
    s_step = 1
    angle_1 = angle_2 = angle_3 = angle_4 = angle_5 = angle_6 = 90

    while True:
        # 게임패드 데이터가 있을 때만 로봇팔을 제어하는 코드 실행
        if gamepad_data is not None:
            try:
                # 게임패드 데이터 파싱
                axis_0 = gamepad_data["axis_0"]
                axis_1 = gamepad_data["axis_1"]
                axis_2 = gamepad_data["axis_2"]
                axis_5 = gamepad_data["axis_5"]
                button_0 = gamepad_data["button_0"]
                button_1 = gamepad_data["button_1"]
                button_2 = gamepad_data["button_2"]
                button_3 = gamepad_data["button_3"]
                button_4 = gamepad_data["button_4"]
                button_5 = gamepad_data["button_5"]
                button_6 = gamepad_data["button_6"]
                button_7 = gamepad_data["button_7"]
                button_8 = gamepad_data["button_8"]

                # 로봇팔 제어 코드 추가
                # ... (기존의 로봇팔 제어 코드를 이곳에 추가)

            except KeyError as e:
                print(f"KeyError: {e}")

        # 임의의 시간 간격으로 반복 수행
        time.sleep(0.05)

# MQTT 클라이언트 설정
client1 = mqtt.Client()
client1.connect("129.254.174.120", 1883, 60)
client1.on_connect = on_connect
client1.on_message = on_message

client2 = mqtt.Client()
client2.connect("129.254.174.120", 9002, 60)
client2.on_connect_socket = on_connect_socket

# 두 개의 쓰레드 생성 및 실행
camera_thread = threading.Thread(target=handle_camera)
gamepad_thread = threading.Thread(target=handle_gamepad)

camera_thread.start()
gamepad_thread.start()