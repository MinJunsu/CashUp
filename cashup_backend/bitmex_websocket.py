import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django
import sys
django.setup()

from data.models import RealTimeData

import websocket
import _thread
import time
import json
from datetime import datetime, timedelta

prev_save_time = None
prev_xbt_usd = 0
prev_xbt_u21 = 0

def on_message(ws, message):
    global prev_save_time, prev_xbt_usd, prev_xbt_u21
    message = json.loads(message)

    table = message.get("table")
    action = message.get("action")
    data = message.get("data")[0]
    if action == "insert":
        print(data)
        if prev_save_time == None:
            prev_save_time = datetime.now()
        if datetime.now() - prev_save_time > timedelta(seconds=1):
            save_data()
            prev_save_time = datetime.now()
        else:
            if data['symbol'] == "XBTUSD":
                prev_xbt_usd = data['bidPrice']
            else:
                prev_xbt_u21 = data['bidPrice']
        if datetime.now() - prev_save_time > timedelta(hours=1):
            ws.close()

def save_data():
    query = RealTimeData.objects.filter(market="bitmex").last()
    query.xbt_usd = prev_xbt_usd
    query.xbt_u21 = prev_xbt_u21
    query.save()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    ws.send('{"op": "subscribe", "args": ["quote:XBTUSD"]}')
    ws.send('{"op": "subscribe", "args": ["quote:XBTU21"]}')

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://www.bitmex.com/realtime",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

ws.run_forever()