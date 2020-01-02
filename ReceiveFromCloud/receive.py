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
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubDeviceClient


async def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = "HostName=Toradex-test-hub.azure-devices.net;DeviceId=colibri-imx8x;SharedAccessKey=s8yOxxvXbYKzQLPVl4B1i9COORghypdR3+lyzvNoSdM="
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    await device_client.connect()

    # define behavior for receiving a message
    async def message_listener(device_client):
        while True:
            message = await device_client.receive_message()  # blocking call
            print("the data in the message received was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)

    # define behavior for halting the application
    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                print("Quitting...")
                break

    # Schedule task for message listener
    asyncio.create_task(message_listener(device_client))

    # Run the stdin listener in the event loop
    Loop = asyncio.get_running_loop()
    user_finished = Loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for messages
    await user_finished

    # Finally, disconnect
    await device_client.disconnect()


if __name__ == "__main__":
    # asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()