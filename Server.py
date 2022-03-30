# Imports 
import time
import paho.mqtt.client as mqtt
import Topics as tp
#Identify the Group
group='G9C_CCS'

#Identify the Topics
topic_1 = tp.PO.PANIC_BUTTON# "G9/CCS/Panic"
topic_2 = "G9/CCS/MOs Code"
topic_3 = tp.CDR.LIGHT_INTENSITY#"G9/CDR/Light Intensity"
topic_4 = tp.CDR.FLOOR_PRESSURE#"G9/CDR/Floor Pressure"
topic_5 = tp.CDR.SEQ_ACCESS#"G9/CDR/Secret Entry"
topic_6 = tp.PO.KNOCK_ACCESS#"G9/CCS/Secret Knock"
topic_7 = tp.CCC.TEMPERATURE#"G9/CCS/Temperature"
topic_8 = tp.CCC.MORSE_ACCESS#"G9/CCS/MOs Code/Granted"
topic_9 = "G9/CCS/MOs Code/Denied"
topic_10 = tp.CCC.TEMPERATURE#"G9/CCC/Temperature"
topic_11 = tp.CCC.MORSE_SEND#"G9/CCC/MOs Code"
topic_12 = "G9/CCS/Alarm"

#Connecting to Server
mqttBroker = "vpn.ce.pdn.ac.lk" #UOP Server
mqttPort = 8883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_11)
    client.subscribe(topic_10)
    client.subscribe(topic_9)
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    Message=str(msg.payload.decode("utf-8"))
    Topic=msg.topic
    print(Topic+"="+Message)
    if Topic==topic_11:
        Mos(Message)
def on_disconnect(client, userdata, rc):
    print("Disconnected")
    client.loop_stop()
    exit()
      
client = mqtt.Client(group) #Group 9C (Control Room)


try:
    client.connect(mqttBroker,mqttPort) 
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect=on_disconnect
    client.loop_start()

except Exception:
    print("Connection to MQTT broker failed!")
    exit(1)

def Mos(message):
    if message=="hello":
        client.publish(topic_8,tp.CCC.ACESS_GRANTED)
        print("Access Granted")
    else:
        client.publish(topic_8,tp.CCC.ACESS_DENIED)
        print("Access Denied")
#client.publish(topic_12,"Fire")

while True:
    time.sleep(0.1)