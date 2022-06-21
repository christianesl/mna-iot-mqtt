#pip install paho-mqtt
#pip install pandas

#importación de librerías
import pandas as pd
import time
import paho.mqtt.client as mqttClient

dataframe=pd.read_csv("DatosPruebaMQTT.csv",index_col=0)
dataframe.head()
dataframe.describe(include="all")
df=dataframe.dropna() #aquí voy a limpiar todos los valores no numéricos

temp=df.Temperature.tolist()
hum=df.Humidity.tolist()
co=df.CO2.tolist()

def on_connect(client, userdata, flags, rc):
    """Función que establece la conexión
    
    """
    if rc==0:
        print("Conectado al broker")
        global Connected
        Connected = True
    else:
        print("Falla en la conexión")
    return

Connected = False  #variable para verificar el estado de la conexión
broker_address="broker.hivemq.com" #dirección del Broker
port=1883 #puerto por defecto de MQTT
tag1 = "/mna29/temp/"  #tag, etiqueta o tópico
tag2 = "/mna29/hum/"  #tag, etiqueta o tópico
tag3 = "/mna29/co2/"  #tag, etiqueta o tópico

client = mqttClient.Client() #instanciación
client.on_connect = on_connect #agregando la función
client.connect(broker_address, port)
client.loop_start() #inicia la instancia

while Connected != True:
    time.sleep(0.1)
    try:
        for i,j,k in zip(temp,hum,co):
            val1,val2,val3='{"Temperatura":"'+str(i)+'"}','{"Humedad":"'+str(j)+'"}','{"CO2":"'+str(k)+'"}'
            print(tag1,val1,'\n',tag2,val2,'\n',tag3,val3)
            client.publish(tag1,val1,qos=2)
            #client.publish(tag2,val2,qos=2)
            #client.publish(tag3,val3,qos=2)
            #client.publish(tag4,val1,qos=2)
            print("localtest")
            time.sleep(2)
    except KeyboardInterrupt: #cuando presionas Ctrl +C
        print("Envío de datos detenido por el usuario")
        client.disconnect()
        client.loop_stop()


#"/MNA/IoT/CompProf/#"

