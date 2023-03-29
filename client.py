import RPi.GPIO as gpio
import paho.mqtt.client as mqtt

## gpio config
gpio.setmode(gpio.BOARD)
out_pin = 16
gpio.setup(out_pin, gpio.OUT) ## GPIO 23

## mqtt config
broker_url = "localhost"
broker_port = 1883

def on_connect(client, userdata, flags, rc):
	print("Connected With Result Code ", rc)

def on_message(client, userdata, message):
	message = message.payload.decode()
	print("Message Recieved: "+message)
	if message == "ON" or message == '1':
		gpio.output(out_pin, True)
		client.publish(topic="gym/access/gate/state", payload="ON", qos=1, retain=False)
	if message == "OFF" or message == '0':
		gpio.output(out_pin, False)
		client.publish(topic="gym/access/gate/state", payload="OFF", qos=1, retain=False)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

client.subscribe("gym/access/gate", qos=1)
client.loop_forever()
