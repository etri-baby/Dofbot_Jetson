import paho.mqtt.client as mqtt
import threading
import base64
import json
import time
import cv2
from Arm_Lib import Arm_Device

with open("config.json", "r") as config_file:
    config = json.load(config_file)

mqtt_broker_ip = config["mqtt_broker"]["ip"]
mqtt_broker_port = config["mqtt_broker"]["port"]
mqtt_socket_broker_ip = config["mqtt_socket_broker"]["ip"]
mqtt_socket_broker_port = config["mqtt_socket_broker"]["port"]


client1 = mqtt.Client()
client2 = mqtt.Client(transport="websockets")

# 게임패드 데이터를 저장할 변수 선언
gamepad_data = None

def on_connect(client1, userdata, flags, rc):
    print("연결 성공, 결과 코드: " + str(rc))
    # 게임패드 데이터 topic 구독
    client1.subscribe("jetson/pad")

def on_connect_socket(client2, userdata, flags, rc):
    if(rc == 0):
        print("Connected to MQTT broker")
        client2.subscribe("jetson/camera")
        client2.subscribe("jetson/read")
    else:
        try_reconnect_socket(client2)
        print("Failed to connect, code: ", rc)

def on_message(client1, userdata, msg):
    global gamepad_data
    # 수신된 메시지 파싱
    
    try:
        payload = msg.payload.decode()
        gamepad_data = json.loads(payload)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

def Arm_Handle():
    client1.connect(mqtt_broker_ip, mqtt_broker_port, 60)
    client1.on_connect = on_connect
    
    if not client1.is_connected:
        try_reconnect(client1)
    else:
        client1.on_message = on_message
    
    client1.loop_start()

def Camera_Handle():
    client2.connect(mqtt_socket_broker_ip, mqtt_socket_broker_port, 60)
    client2.on_connect = on_connect_socket
    if not client2.is_connected:
        try_reconnect_socket(client2)
    else:
        camera(client2)
        
    client2.loop_start()

def camera(client2):
    image = cv2.VideoCapture(0)
    image.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    image.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    try:
        while True:
            ######### Servo 데이터 발행 #########
            arm_data = []
            for i in range(6):
                aa = Arm.Arm_serial_servo_read(i+1)
                arm_data.append({i+1: str(aa)})
            client2.publish("jetson/read", json.dumps(arm_data))
            ######### Servo 데이터 발행 #########

            ret, frame = image.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_base64 = base64.b64encode(buffer).decode()
                client2.publish("jetson/camera", jpg_base64, qos=0)

    except KeyboardInterrupt:
        print("카메라 처리 종료")
        image.release()

def arm():
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

                if axis_1 <= 0.1 and axis_1 >= -0.1:
                    time.sleep(.000001)
                else:
                    if axis_1 > 0.1:
                        angle_2 += s_step
                    else:
                        angle_2 -= s_step
                    if angle_2 > 180:
                        angle_2 = 180
                    elif angle_2 < 0:
                        angle_2 = 0
                    Arm.Arm_serial_servo_write(2, angle_2, s_time)
                    time.sleep(0.05)

                # No.1 servo, A0 Left-negative Right-positive
                if axis_0 <= 0.1 and axis_0 >= -0.1:
                    time.sleep(.000001)
                else:
                    if axis_0 > 0.1:
                        angle_1 -= s_step
                    else:
                        angle_1 += s_step

                    if angle_1 > 180:
                        angle_1 = 180
                    elif angle_1 < 0:
                        angle_1 = 0
                    Arm.Arm_serial_servo_write(1, angle_1, s_time)
                    time.sleep(0.05)

                # No.6 servo, NUM1=B0,NUM3=B2, A2 Up-negative Down-positive
                if button_0:
                    angle_6 += s_step
                    if angle_6 > 180:
                        angle_6 = 180
                    elif angle_6 < 0:
                        angle_6 = 0
                    Arm.Arm_serial_servo_write(6, angle_6, s_time)
                    time.sleep(0.05)
                elif button_2:
                    angle_6 -= s_step
                    if angle_6 > 180:
                        angle_6 = 180
                    elif angle_6 < 0:
                        angle_6 = 0
                    Arm.Arm_serial_servo_write(6, angle_6, s_time)
                    time.sleep(0.05)
                elif axis_2 > 0.5:
                    angle_6 -= s_step
                    if angle_6 > 180:
                        angle_6 = 180
                    elif angle_6 < 0:
                        angle_6 = 0
                    Arm.Arm_serial_servo_write(6, angle_6, s_time)
                    time.sleep(0.05)
                elif axis_2 < -0.5:
                    angle_6 += s_step
                    if angle_6 > 180:
                        angle_6 = 180
                    elif angle_6 < 0:
                        angle_6 = 0
                    Arm.Arm_serial_servo_write(6, angle_6, s_time)
                    time.sleep(0.05)

                # No.5, NUM2=B1,NUM4=B3, A5Left-negative Right-positive
                if button_1:
                    angle_5 += s_step
                    if angle_5 > 180:
                        angle_5 = 180
                    elif angle_5 < 0:
                        angle_5 = 0
                    Arm.Arm_serial_servo_write(5, angle_5, s_time)
                    time.sleep(0.05)
                elif button_3:
                    angle_5 -= s_step
                    if angle_5 > 180:
                        angle_5 = 180
                    elif angle_5 < 0:
                        angle_5 = 0
                    Arm.Arm_serial_servo_write(5, angle_5, s_time)
                    time.sleep(0.05)
                elif axis_5 > 0.5:
                    angle_5 += s_step
                    if angle_5 > 180:
                        angle_5 = 180
                    elif angle_5 < 0:
                        angle_5 = 0
                    Arm.Arm_serial_servo_write(5, angle_5, s_time)
                    time.sleep(0.05)
                elif axis_5 < -0.5:
                    angle_5 -= s_step
                    if angle_5 > 180:
                        angle_5 = 180
                    elif angle_5 < 0:
                        angle_5 = 0
                    Arm.Arm_serial_servo_write(5, angle_5, s_time)
                    time.sleep(0.05)

                # NO.4 servo，R1=B5,R2=B7
                if button_5:
                    angle_4 -= s_step
                    if angle_4 > 180:
                        angle_4 = 180
                    elif angle_4 < 0:
                        angle_4 = 0
                    Arm.Arm_serial_servo_write(4, angle_4, s_time)
                    time.sleep(0.05)
                elif button_7:
                    angle_4 += s_step
                    if angle_4 > 180:
                        angle_4 = 180
                    elif angle_4 < 0:
                        angle_4 = 0
                    Arm.Arm_serial_servo_write(4, angle_4, s_time)
                    time.sleep(0.05)

                # NO.3 servo，L1=B4,L2=B6
                if button_4:
                    angle_3 -= s_step
                    if angle_3 > 180:
                        angle_3 = 180
                    elif angle_3 < 0:
                        angle_3 = 0
                    Arm.Arm_serial_servo_write(3, angle_3, s_time)
                    time.sleep(0.05)
                elif button_6:
                    angle_3 += s_step
                    if angle_3 > 180:
                        angle_3 = 180
                    elif angle_3 < 0:
                        angle_3 = 0
                    Arm.Arm_serial_servo_write(3, angle_3, s_time)
                    time.sleep(0.05)

                # Press the key B8 to set all servos of DOFBOT to 90 degrees
                if button_8:
                    angle_1 = angle_2 = angle_3 = angle_4 = angle_5 = angle_6 = 90
                    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
                    time.sleep(1)

            except KeyError as e:
                print(f"KeyError: {e}")

def try_reconnect(client):
    while not client.is_connected():
        try:
            print("Trying to mqtt socket reconnect...")
            client.connect(mqtt_broker_ip, mqtt_broker_port, 60)
            time.sleep(3)
        except ConnectionError:
            print("Failed to reconnect. Retrying in 3 seconds...")
            time.sleep(3)

def try_reconnect_socket(client):
    while not client.is_connected():
        try:
            print("Trying to mqtt reconnect...")
            client.connect(mqtt_socket_broker_ip, mqtt_socket_broker_port, 60)
            time.sleep(3)
        except ConnectionError:
            print("Failed to reconnect. Retrying in 3 seconds...")
            time.sleep(3)


Arm = Arm_Device()

t1 = threading.Thread(target=Arm_Handle)
t2 = threading.Thread(target=Camera_Handle)

t1.start()
t2.start()

arm()