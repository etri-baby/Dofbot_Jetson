import paho.mqtt.client as mqtt
import json
import time

# MQTT Broker 주소와 포트 설정
broker_address = "raspberry_pi_ip_address"
broker_port = 1883

# MQTT 클라이언트 생성
client = mqtt.Client()

# MQTT 메시지를 수신할 때 호출되는 콜백 함수
def on_message(client, userdata, message):
    gamepad_input = json.loads(message.payload)
    print("게임패드 입력 받음:", gamepad_input)
    # 게임패드 입력 값들을 이용하여 로봇팔 제어 코드를 작성
    # ... 로봇팔 제어 코드 ...

# 콜백 함수를 설정하고 MQTT Broker에 연결
client.on_message = on_message
client.connect(broker_address, broker_port)

# gamepad_input topic으로 메시지를 구독
client.subscribe("my/topic")

# 메시지를 받아오기 위해 계속 루프를 돈다
client.loop_forever()