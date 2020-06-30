import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "dcwm2n"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        i=random.randint(0,5)
        v=random.randint(200,230)
        p=v*i
        data = { 'Current' : str(i)+'A', 'Voltage': str(v)+'V', 'Power' : str(p)+'W'}
        print (data)
        def myOnPublishCallback():
            print ("Published Current = %s A" % i, "Voltage = %s V" % v,"Power = %s W" %p, "to IBM Watson")

        success = deviceCli.publishEvent("Energy Meter", "json", data , qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
