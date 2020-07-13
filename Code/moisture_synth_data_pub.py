import time
from synth_m_data import MoistureSensor
import paho.mqtt.client as MQTT


broker_address = "127.0.0.1"
port=1883
keepalive_time = 60
interval = 1

def main():

    mqttclient = MQTT.Client(client_id='publisher_moisture')
    mqttclient.connect(broker_address,port,keepalive_time)

    ms = MoistureSensor(40, 30, 10, 90)
    while True:
        mois_val = ms.sense()
        print(ms.sensorType,mois_val)
        mqttclient.publish("sensors/health/moisture",mois_val)
        #delay of 1 seconds
        time.sleep(interval)


if __name__ == '__main__':

    main()


