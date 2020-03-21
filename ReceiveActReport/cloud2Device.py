# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# This program is inspired from https://github.com/Azure/azure-iot-sdk-python-preview/blob/master/azure-iot-device/samples/advanced-hub-scenarios/receive_message.py

# TESTING
# In Azure IOT use the following command to send message, that will be recived by this program.
# `az iot device c2d-message send --device-id colibri-imx8x --hub-name Toradex-test-hub --data "Hello! This is Programmer."`

import os
import io
import time
import uuid
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message


async def main():
    # Though the Conn string is always recommended to rx from teh Env. for convenience sake, wee enter here.
    conn_str = "HostName=Toradex-test-hub.azure-devices.net;DeviceId=colibri-imx8x;SharedAccessKey=s8yOxxvXbYKzQLPVl4B1i9COORghypdR3+lyzvNoSdM="
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    await device_client.connect()

    # define behavior for receiving a message
    async def message_listener(device_client):
        
        export_file2 = "/sys/class/gpio/export"
        f = io.open(export_file2, "w")         
        f.write("407")                
        f.close()     
         
        time.sleep(1)
        export_file3 = "/sys/class/gpio/gpio407/direction"
        f = io.open(export_file3, "w")                    
        f.write("out")                
        f.close()
        print("I am in device_client")
        
        print("Enter start to get the LEDs blinking  ")
        message = await device_client.receive_message()  # blocking call
        print(message.data.decode("utf-8") )

        print("Check:" + message.data.decode("utf-8").lower()  == "Start".lower())

        if(message.data.decode("utf-8").lower()  == "Start".lower()):      
            print("Blinking LED")     
            sender = asyncio.get_event_loop() 
            while True:
                # Blinking_LED.py part
                # export_file = "/sys/class/gpio/gpio407/value"
                # f = io.open(export_file, "w")                
                # f.write("1")    
                # f.close()
                sender.create_task(send_test_message(1))                    
                time.sleep(0.5)
                      
                # export_file = "/sys/class/gpio/gpio407/value"
                # f = io.open(export_file, "w")                
                # f.write("0")                 
                # f.close()
                sender.create_task(send_test_message(0))                   
                time.sleep(0.5)
        else:
            print("Unknown Data received. Received Data = " + message.data)
    
    async def send_test_message(i):
        print("sending message" + str(i))
        msg = Message("{ \"state\": " + str(i) + "}")
        msg.message_id = uuid.uuid4()
        msg.correlation_id = "correlation-1234"
        await device_client.send_message(msg)
        print("done sending message #" + str(i))

    # define behavior for halting the application
    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                #Blinking_LED.py part: Unexport the pin
                export_file2 = "/sys/class/gpio/unexport"
                f = io.open(export_file2, "w")           
                f.write("407")
                print("Quitting...")
                break
    listener = asyncio.get_event_loop(0)
    # Schedule task for message listener
    listener.create_task(message_listener(device_client))

    # Run the stdin listener in the event loop
    #Loop = asyncio.get_running_loop()
    user_finished = listener.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for messages
    await user_finished

    # Finally, disconnect
    await device_client.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
