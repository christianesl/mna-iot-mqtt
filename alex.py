import pandas as pd
import paho.mqtt.client as mqtt
import time
from random import randint
import os
import json

df = pd.read_csv('https://raw.githubusercontent.com/Alex980102/mqtt_MNA_A4/main/db/DatosPruebaMQTT.csv', index_col=0)
df

temp = df.Temperature
hum = df.Humidity
co = df.CO2

Connected = True
mqttBroker = "broker.hivemq.com"
tag = "mna09"
client = mqtt.Client()
client.connect(mqttBroker)

while Connected != False:
    try:
        for i,j,k in zip(temp, hum, co):
            publicar = {
                "Temperatura": i,
                "Humedad": j,
                "C02": k
            }
            publicar = json.dumps(publicar)
            client.publish(tag, publicar)
            print(f"Just published {publicar} al topic {tag}")
            time.sleep(1)
    except KeyboardInterrupt:
        print('Sesión interrumpida')
        client.disconnect()
        Connected = False