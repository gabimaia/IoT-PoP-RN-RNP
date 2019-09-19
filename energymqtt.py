import os
import time
import sys
#import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = '192.168.70.203'
ACCESS_TOKEN = '4d5LLaL1rjN3aJTzYUbS'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

#sensor_data = {'corrente': 0, 'tensao': 0, 'potencia': 0}

sensor_data2 = {'corrente': 0, 'tensao': 0, 'potencia': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        corrente = os.popen('sudo mosquitto_sub -C 1 -u aluno -P alunopop -t testeSCT').read()
        tensao = os.popen('sudo mosquitto_sub -C 1 -u aluno -P alunopop -t testeP8').read()
        potencia = os.popen('sudo mosquitto_sub -C 1 -u aluno -P alunopop -t testepower').read()
        print(corrente, tensao, potencia)
        #corrente = round(corrente,2)
        #tensao = round(tensao,2)
        #potencia = round(potencia,2)
        #break
        #print(u"Corrente: {:g}\u00b0C, tensao: {:g}\u00b0C, potencia: {:g}%".format(corrente, tensao, potencia))
        sensor_data2['corrente'] = corrente
        sensor_data2['tensao'] = tensao
        sensor_data2['potencia'] = potencia

        # Sending humidity and temperature data to ThingsBoard
        #print("publish topic", json.dumps(sensor_data))
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data2,0))
        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
