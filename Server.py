# Imports 
import time
import paho.mqtt.client as mqtt

#Import Your Python File
import Test #Only for test

#Identify the Group
group='G9C'

#Identify the Topics
topic_Test_s = "Test/s"
topic_Test_r = "Test/r"
topic_1 = "Panic"
topic_2 = "MOs Code"
topic_3 = "Light Intensity"
topic_4 = "Floor Pressure"
topic_5 = "Secret Entry"
topic_6 = "Secret Knock"
topic_7 = "Temperature"

#Connecting to Server
mqttBroker = "vpn.ce.pdn.ac.lk" #UOP Server
mqttPort = 8883

#Global Variable
Message=None
Topic=None

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_Test_s)
    client.subscribe(topic_Test_r)
    '''client.subscribe(topic_1)
    client.subscribe(topic_2)
    client.subscribe(topic_3)
    client.subscribe(topic_4)
    client.subscribe(topic_5)
    client.subscribe(topic_6)
    client.subscribe(topic_7)'''
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    global Message
    global Topic
    Message=str(msg.payload.decode("utf-8"))
    Topic=msg.topic
#This Fucntion distribute the the Message to the Relevant Functions
def Distributer(Topic,Message):
    if Topic==topic_Test_r:
        #Enter the Relavant fucntion name for the Panic
        #for the test It use Resistor Function
        Test.LED(Message)
    '''if Topic==topic_1:
        #Enter the relavant Function name for the Panic
    elif Topic==topic_2:
        #Enter the relavant Function name for the Mos Code
    elif Topic==topic_3:
        #Enter the relavant Function name for the Light Intensity
    elif Topic==topic_4:
        #Enter the relavant Function name for the Floor Pressure
    elif Topic==topic_5:
        #Enter the relavant Function name for the Secret Entry
    elif Topic==topic_6:
        #Enter the relavant Function name for the Secret Knock
    elif Topic==topic_7:
        #Enter the relavant Function name for the Temperature
    else:
        pass'''
        
client = mqtt.Client(group) #Group 9C (Control Room)


try:
    client.connect(mqttBroker,mqttPort) 
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
except:
    print("Connection to MQTT broker failed!")
    exit(1)

while True:
    #For the Test
    value_test=Test.resistor_1()
    #value_Panic='...............'
    #value_MOs Code='...............'
    #value_Light Intensity='...............'
    #value_Floor Pressure='...............'
    #value_Secret Entry='...............'
    #value_Secret Knock='...............'
    #value_Temperature='...............'
    time.sleep(0.1)
    client.publish(topic_Test_s,value_test)
    #client.publish(topic_1,value_Panic)
    #client.publish(topic_2,value_MOs Code)
    #client.publish(topic_3,value_Light Intensity)
    #client.publish(topic_4,value_Floor Pressure)
    #client.publish(topic_5,value_Secret Entry)
    #client.publish(topic_6,value_Secret Knock)
    #client.publish(topic_7,value_Temperature)'''
    Distributer(Topic,Message)
    print(Topic,Message)
    
    
