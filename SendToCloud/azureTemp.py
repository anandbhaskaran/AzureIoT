from base64 import b64encode, b64decode
from hashlib import sha256
from urllib.parse import quote_plus, urlencode, quote
from hmac import HMAC
import requests
import json
import os
import time
 
# Temperature Sensor
# BASE_DIR = '/sys/bus/w1/devices/'
# SENSOR_DEVICE_ID = 'YOUR_DEVICE_ID'
# DEVICE_FILE = BASE_DIR + SENSOR_DEVICE_ID + '/w1_slave'

# Azure IoT Hub
URI = 'Toradex-test-hub.azure-devices.net'
KEY = '2dd9JTH5NO0baFz/5SCheiyl9/Ub7xSsnuo608cL6Uw='
IOT_DEVICE_ID = 'colibri-imx8x'
POLICY = 'iothubowner'

def generate_sas_token():
    expiry = 10000
    ttl = str(int(time.time() + expiry))
    uri = '{0}/devices/{1}'.format(URI, IOT_DEVICE_ID)
    sign_key = "%s\n%s" % ((quote_plus(uri)), ttl)
    signature = b64encode(HMAC(b64decode(KEY), sign_key.encode('utf-8'), sha256).digest())
    

    rawtoken = {
        'sr' : uri,
        'sig': signature,
        'se' : ttl
    }

    rawtoken['skn'] = POLICY

    return 'SharedAccessSignature ' + urlencode(rawtoken)

def read_temp_raw():
    # f = open(DEVICE_FILE, 'r')
    # lines = f.readlines()
    # f.close()
    # return lines
    return 45


def send_message(token, message):
    url = 'https://{0}/devices/{1}/messages/events?api-version=2016-11-14'.format(URI, IOT_DEVICE_ID)
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    data = json.dumps(message)
    response = requests.post(url, data=data, headers=headers)
    if(response.status_code == 204):
        print("Message sent to azure successfully")

if __name__ == '__main__':
    # 1. Enable Temperature Sensor
    # os.system('modprobe w1-gpio')
    # os.system('modprobe w1-therm')

    # 2. Generate SAS Token
    token = generate_sas_token()

    # 3. Send Temperature to IoT Hub
    while True:
        temp = 45
        message = { "temp": str(temp) }
        send_message(token, message)
        time.sleep(1)
