import paho.mqtt.client as mqtt
import ipywidgets.widgets as widgets
import threading
import json
import time
import inspect
import ctypes
from Arm_Lib import Arm_Device
from IPython.display import display

# 게임패드 데이터를 저장할 변수 선언
gamepad_data = None

def on_connect(client, userdata, flags, rc):
    print("연결 성공, 결과 코드: " + str(rc))
    # 라즈베리 파이가 게임패드 데이터를 발행하는 주제(topic)를 구독
    client.subscribe("my/topic")

def on_message(client, userdata, msg):
    global gamepad_data
    # 수신된 메시지 파싱
    try:
        payload = msg.payload.decode()
        gamepad_data = json.loads(payload)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

def Arm_Handle():
    # MQTT 클라이언트 설정
    client = mqtt.Client()
    client.connect("129.254.174.120", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

Arm = Arm_Device()
thread2 = threading.Thread(target=Arm_Handle)
thread2.start()

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
                time.sleep(0.01)

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
                time.sleep(0.01)

            # No.6 servo, NUM1=B0,NUM3=B2, A2 Up-negative Down-positive
            if button_0:
                angle_6 += s_step
                if angle_6 > 180:
                    angle_6 = 180
                elif angle_6 < 0:
                    angle_6 = 0
                Arm.Arm_serial_servo_write(6, angle_6, s_time)
                time.sleep(0.01)
            elif button_2:
                angle_6 -= s_step
                if angle_6 > 180:
                    angle_6 = 180
                elif angle_6 < 0:
                    angle_6 = 0
                Arm.Arm_serial_servo_write(6, angle_6, s_time)
                time.sleep(0.01)
            elif axis_2 > 0.5:
                angle_6 -= s_step
                if angle_6 > 180:
                    angle_6 = 180
                elif angle_6 < 0:
                    angle_6 = 0
                Arm.Arm_serial_servo_write(6, angle_6, s_time)
                time.sleep(0.01)
            elif axis_2 < -0.5:
                angle_6 += s_step
                if angle_6 > 180:
                    angle_6 = 180
                elif angle_6 < 0:
                    angle_6 = 0
                Arm.Arm_serial_servo_write(6, angle_6, s_time)
                time.sleep(0.01)

            # No.5, NUM2=B1,NUM4=B3, A5Left-negative Right-positive
            if button_1:
                angle_5 += s_step
                if angle_5 > 180:
                    angle_5 = 180
                elif angle_5 < 0:
                    angle_5 = 0
                Arm.Arm_serial_servo_write(5, angle_5, s_time)
                time.sleep(0.01)
            elif button_3:
                angle_5 -= s_step
                if angle_5 > 180:
                    angle_5 = 180
                elif angle_5 < 0:
                    angle_5 = 0
                Arm.Arm_serial_servo_write(5, angle_5, s_time)
                time.sleep(0.01)
            elif axis_5 > 0.5:
                angle_5 += s_step
                if angle_5 > 180:
                    angle_5 = 180
                elif angle_5 < 0:
                    angle_5 = 0
                Arm.Arm_serial_servo_write(5, angle_5, s_time)
                time.sleep(0.01)
            elif axis_5 < -0.5:
                angle_5 -= s_step
                if angle_5 > 180:
                    angle_5 = 180
                elif angle_5 < 0:
                    angle_5 = 0
                Arm.Arm_serial_servo_write(5, angle_5, s_time)
                time.sleep(0.01)

            # NO.4 servo，R1=B5,R2=B7
            if button_5:
                angle_4 -= s_step
                if angle_4 > 180:
                    angle_4 = 180
                elif angle_4 < 0:
                    angle_4 = 0
                Arm.Arm_serial_servo_write(4, angle_4, s_time)
                time.sleep(0.01)
            elif button_7:
                angle_4 += s_step
                if angle_4 > 180:
                    angle_4 = 180
                elif angle_4 < 0:
                    angle_4 = 0
                Arm.Arm_serial_servo_write(4, angle_4, s_time)
                time.sleep(0.01)

            # NO.3 servo，L1=B4,L2=B6
            if button_4:
                angle_3 -= s_step
                if angle_3 > 180:
                    angle_3 = 180
                elif angle_3 < 0:
                    angle_3 = 0
                Arm.Arm_serial_servo_write(3, angle_3, s_time)
                time.sleep(0.01)
            elif button_6:
                angle_3 += s_step
                if angle_3 > 180:
                    angle_3 = 180
                elif angle_3 < 0:
                    angle_3 = 0
                Arm.Arm_serial_servo_write(3, angle_3, s_time)
                time.sleep(0.01)

            # Press the key B8 to set all servos of DOFBOT to 90 degrees
            if button_8:
                angle_1 = angle_2 = angle_3 = angle_4 = angle_5 = angle_6 = 90
                Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
                time.sleep(1)

        except KeyError as e:
            print(f"KeyError: {e}")
    
    # 임의의 시간 간격으로 반복 수행
    time.sleep(0.1)
