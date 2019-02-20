import math
import smbus
import time
import json
import paho.mqtt.client as mqtt
import struct

bus = smbus.SMBus(1)
bus_temp = smbus.SMBus(1)

def readtemp():
	#CCS811 and TMP006 are made to face each other
	#Vobj is the voltage linked to the temperature of the object (CCS811), register 0
	Vobj = bus_temp.read_i2c_block_data(0x40,0x00,2) 
	
	#reads temperature of the die (semiconducting material in TMP006 chip), register 1
    Tdie = bus_temp.read_i2c_block_data(0x40,0x01,2) 
	#Converting bytes to decimal numbers
    Vobj = Vobj[0]*256+Vobj[1] 
	Tdie = Tdie[0]*256+Tdie[1]
	#LSB corresponds to 156.25nV  
    Vobj= Vobj*(156.25*10**-9)
	#LSB corresponds to 1/32 of a celsius degree and byte needs to be shifted by 2 (divided by 4)
	#1/(32*4)=1/128
    Tdie = Tdie/128
	#Constants given by TMP006 datasheet
	a1 = 1.75*10**-3
    a2 = -1.678*10**-5
    Tref = 298.15
    b0 = -2.94*10**-5
    b1 = -5.7*10**-7
    b2 = 4.63*10**-9
    c2 = 13.4
    #Calibration factor
	S0 = 6*10**-13
	#Offset voltage due to self-heating of TMP006
	Vos = b0 + b1*(Tdie) + b2*(Tdie)**2
	#Model of the Seebeck coefficients of the thermopile and how they change over temperature
    f_Vobj = (Vobj-Vos)+c2*(Vobj-Vos)**2
	#Sensitivity of the thermopile sensor and how it changes over temperature
    S = S0*(1+(a1*(Tdie-25))+a2*(Tdie-25)**2)
    #Link between the radiant transfer of IR energy between CCS811 and TMP006 and the conducted heat in the thermopile in TMP006 to find the temperature of CCS811 in Kelvins
	Tobj = ((Tdie**4 + f_Vobj/S)**(1/4))-273.15
    return Tobj;


def updatetemp(temperature,humidity):
	#Can pass humidity value if known, TMP006 only measures temperature
	#LSB represents 1/512 of a percent in humidity 
    humidity = int(humidity * 512)
	#LSB represents 1/512 of a degree celsius with an offset of 25 degrees
    temperature = int((temperature + 25) * 512)
    #Create an empty byte array with size 4
	buf = bytearray(4)
	#Pack humidity and temperature values into byte array
    struct.pack_into(">HH", buf, 0, humidity, temperature)
	#Convert byte array into list
	envlist=list(buf)
	#Write the list to the ENV_DATA, register 0x05
	bus.write_i2c_block_data(0x5b,0x05,envlist)
	time.sleep(0.1)

		
def readdata():
	#Read the measured CO2 and TVOC levels
	data = bus.read_i2c_block_data(0x5b,0x02,4)
    time.sleep(0.2)
	#Convert bytes into decimal numbers
    CO2 = data[0]*256 + data[1]
    TVOC = data[2]*256 + data[3]
    return CO2,TVOC;

def attemptconnect(client):
	try:
		#The following line is only needed when using encrypted port 8884  
		#client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
		client.connect("ee-estott-octo.ee.ic.ac.uk",port=1883)
        #sets connected_flag to true if no exception is thrown
        client.connected_flag=True
	except:
		print("connection failed")


		
#connecting to the MQTT client
client = mqtt.Client()
#Initialize to false the member variable used to check connection with the broker
mqtt.Client.connected_flag=False
#The following line is only needed when using encrypted port 8884  
#client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
client.subscribe("IC.embedded/leshabibis/1")

#waiting for connection to be established
while (not client.connected_flag):
    print("Attempting to connect to broker")
    attemptconnect(client)
	time.sleep(1)

while(1):
	Tobj = readtemp()
	#Default humidity is 50%
    updatetemp(Tobj,50) 
    CO2,TVOC=readdata()
    DataDict = {"CO2": CO2, "TVOC": TVOC}
    readings = json.dumps(DataDict)
    client.publish("IC.embedded/leshabibis/1",readings)
    print(readings)
    time.sleep(0.8)


