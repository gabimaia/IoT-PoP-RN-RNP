import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json

THINGSBOARD_HOST = '192.168.70.203'
ACCESS_TOKEN = '4d5LLaL1rjN3aJTzYUbS'

pino_1 = 11
pino_2 = 15
pino_3 = 3

# We assume that all GPIOs are LOW
gpio_state = {pino_1: False, pino_2: False, pino_3: False}


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current GPIO status
    client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print 'Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload)
    # Decode JSON request
    data = json.loads(msg.payload)
    print data['params']
    print data['method']
    # Check request method
    if data['method'] == 'getValue':
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        # Reply with GPIO status
        #set_gpio_status(11,'disable')
        #client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        #client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
        #client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
    elif data['method'] == 'setValue':
        print 'ok'
        # Update GPIO status and reply
        set_gpio_status(pino_1, data['params'])
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
    if data['method'] == 'getValue1':
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        # Reply with GPIO status
        #set_gpio_status(11,'disable')
        #client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        #client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
        #client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
    elif data['method'] == 'setValue1':
        print 'ok'
        # Update GPIO status and reply
        set_gpio_status(pino_2, data['params'])
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
    if data['method'] == 'getValue2':
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        # Reply with GPIO status
        #set_gpio_status(11,'disable')
        #client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        #client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
        #client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
    elif data['method'] == 'setValue2':
        print 'ok'
        # Update GPIO status and reply
        set_gpio_status(pino_3, data['params'])
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        client.publish('v1/devices/me/attributes', get_gpio_status(), 1)

def get_gpio_status():
    # Encode GPIOs state to json
    return json.dumps(gpio_state)


def set_gpio_status(pin, status):
    # Output GPIOs state
    GPIO.output(pin, GPIO.HIGH if status==True else GPIO.LOW)
    print 'gpio is high'
    # Update GPIOs state
    gpio_state[pin] = status


# Using board GPIO layout
GPIO.setmode(GPIO.BOARD)
for pin in gpio_state:
    # Set output mode for all GPIO pins
    GPIO.setup(pin, GPIO.OUT)

client = mqtt.Client()
# Register connect callback
client.on_connect = on_connect
# Registed publish message callback
client.on_message = on_message
# Set access token
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
