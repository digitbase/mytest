import paho.mqtt.client as mqtt
import json
import time
import datetime

currtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# MQTT 服务器信息
# BROKER = "222.221.241.110"
# PORT = 1883

BROKER = "112.126.72.58"
PORT = 18885

TOPIC = "111/222"
USERNAME = "530000189992"
PASSWORD = "6daf67283cdc750114a2"

# 连接回调
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# 创建 MQTT 客户端
client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect

# 连接服务器
client.connect(BROKER, PORT, 60)

# 模拟设备数据发送
while True:
    payload = {
        "device_id": "sensor_001",
        "temperature": currtime
    }
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print(f"Published: {payload}")
    time.sleep(5)  # 每 15 秒发送一次