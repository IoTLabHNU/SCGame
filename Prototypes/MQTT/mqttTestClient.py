#MQTT TestmqttClient GUI
import tkinter as tk
from tkinter import *
import paho.mqtt.client as mqtt
from clientData import ClientData


CONST_TOPIC_START_ROUND = "startRound"
CONST_TOPIC_STOP_ROUND = "stopRound"
CONST_TOPIC_SEND_DATA = "sendData"
CONST_TOPIC_REGISTER = "register"


#Connect to Server
def process_connect2Server():
    bt_connect2Server.config(state = "disabled")     
    entry_number.config(state = "disabled")    
    ##connect 2 MQTTServer:  
    mqttClient.connect("broker.hivemq.com", 1883, 60)
    mqttClient.loop_start()

#after connection was established
def on_connect(mqttClient, userdata, flags, rc):
    label_connectionState.config(text = "connected")
    #subscribe for topics
    mqttClient.subscribe(CONST_TOPIC_START_ROUND, 0)
    mqttClient.subscribe(CONST_TOPIC_STOP_ROUND, 0)
    #register  myClient
    myClientData.id = str(entry_number.get())
    s = myClientData.obj2JSON()
    ok = mqttClient.publish(CONST_TOPIC_REGISTER, s)

    
#Reseive messages: startRound, stopRound
def on_message(mosq, obj, msg):
    try: 
        if msg.topic.startswith(CONST_TOPIC_START_ROUND):
            
            s = str(msg.payload).replace('b', '')
            s = s.replace('\'', '')
            o = ClientData.json2obj(s)

            if (o.id == myClientData.id):
                #TODO: find a better way for copy a object
                myClientData.id=o.id
                myClientData.order=o.order
                myClientData.delivery=o.delivery
                myClientData.roundNr=o.roundNr
                myClientData.stock_ig=o.stock_ig
                myClientData.stock_fg=o.stock_fg

                label_roundState.config(text = "runnning")
                label_roundNr.config(text = str(myClientData.roundNr))
                label_deliveryData.config(text = "delivery (" + str(myClientData.delivery)+ ")")
                label_orderData.config(text = "order (" + str(myClientData.order) + ")")
                switchGUI("normal")

        if msg.topic.startswith(CONST_TOPIC_STOP_ROUND):
            label_roundState.config(text = "stopped")
            switchGUI("disabled")
                
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2])
        

#Send data from mqttClient to Admin via Server
def process_sendData():
    myClientData.order = entry_orderData.get()
    myClientData.delivery = entry_deliveryData.get()
    s = myClientData.obj2JSON()
    ok = mqttClient.publish(CONST_TOPIC_SEND_DATA, s)


#disable all widgets
def switchGUI(s):   #s="disabled" or "normal"
    label_roundNr.config(state = s)
    label_roundInfo.config(state = s)
    label_ID.config(state = s)
    label_orderData.config(state = s)
    entry_orderData.config(state = s)
    label_deliveryData.config(state = s)
    entry_deliveryData.config(state = s)
    bt_sendData.config(state = s)
    label_roundState.config(state = s)


#Main-Program
myClientData = ClientData() #container for all relevant data for the mqttClient
mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message

win = tk.Tk()
win.title("TEST MQTT")
win.geometry("500x180")

#widgets --------------------------------------------------------

#Label
label_ID = tk.Label(win, text="ID:")
label_ID.grid(column=0, row=0)

#entry for myClient ID
entry_number = tk.Entry()
entry_number.grid(column=1, row=0)

#Button connect
bt_connect2Server = tk.Button(text="Connect to Server", command=process_connect2Server)
bt_connect2Server.grid(column=2, row=0)

label_connectionState = tk.Label(win, text="")
label_connectionState.grid(column=3, row=0)    

label_roundInfo = tk.Label(win, text="Actual Round:")
label_roundInfo.grid(column=0, row=1)   

label_roundNr = tk.Label(win, text="")
label_roundNr.grid(column=1, row=1)  

label_roundState = tk.Label(win, text="")
label_roundState.grid(column=2, row=1)  

label_orderData = tk.Label(win, text="order:")
label_orderData.grid(column=0, row=2)   

entry_orderData = tk.Entry()
entry_orderData.grid(column=1, row=2)

label_deliveryData = tk.Label(win, text="delivery:")
label_deliveryData.grid(column=0, row=3)   

entry_deliveryData = tk.Entry()
entry_deliveryData.grid(column=1, row=3)

#Button send data
bt_sendData = tk.Button(text="Send Data", command=process_sendData)
bt_sendData.grid(column=0, row=4)  

switchGUI("disable")

#start the event-loop of main-Windows-----------------------------
win.mainloop()


