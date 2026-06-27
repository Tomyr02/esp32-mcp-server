import json
import urllib.request
import os

FIREBASE_URL = os.environ['FIREBASE_URL']
FIREBASE_SECRET = os.environ['FIREBASE_SECRET']

def lambda_handler(event, context):
    # El evento llega directamente del ESP32 via IoT Rule
    data = {
        'deviceId':    event.get('deviceId', ''),
        'temperatura': event.get('temperatura', 0),
        'presion':     event.get('presion', 0),
        'timestamp':   event.get('timestamp', 0)
    }

    url = f"{FIREBASE_URL}/sensores.json?auth={FIREBASE_SECRET}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        method='POST',
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
    print(f"Enviado a Firebase: {data}")

    return {'statusCode': 200}