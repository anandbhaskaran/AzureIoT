# Azure IOT 

This repo contains working examples for Azure IOT communication.

## 1. Send To Cloud
This will send the message to cloud using Python

## 2. Recive from Cloud   
This will recieve messages that are triggered in the Azure IOT 

## 3. Web Apps Node IOT Hub
A cloned repo that helps us to monitor the messages sent to cloud

## 4. Receive Act React
Issue the following command to initiate the action:
`az iot device c2d-message send --device-id colibri-imx8x --hub-name Toradex-test-hub --data "Start"`

1. Receive a message
2. If right message act by blinking LED
3. Report the LED State back to the cloud

Debug Command (Cross check the recieved messages in Azure CLI)
`az iot hub monitor-events --hub-name Toradex-test-hub --output table`