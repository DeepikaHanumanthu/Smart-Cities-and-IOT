
import paho.mqtt.client as MQTT #import the client

# Function to process recieved message
def process_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain) 



# Create client
client = MQTT.Client(client_id="subscriber-1")

# Assign callback function
client.on_message = process_message

# Connect to broker
client.connect("127.0.0.1",1883,60)

# Subscriber to topic
client.subscribe("sensors/#")

# Run loop
client.loop_forever()
