import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django
import sys
django.setup()

from data.models import RealTimeData

import websocket
import json
from datetime import datetime, timedelta


query = RealTimeData.objects.filter(market="bitmex").last()

prev_save_time = None
initial_time = None
prev_xbt_usd = query.xbt_usd
prev_xbt_sub = query.xbt_sub
prev_usd_bid = query.bid_usd
prev_usd_ask = query.ask_usd
prev_sub_bid = query.bid_sub
prev_sub_ask = query.ask_sub

def on_message(ws, message):
    global prev_save_time, initial_time, prev_xbt_usd, prev_xbt_sub, prev_usd_bid, prev_usd_ask, prev_sub_bid, prev_sub_ask
    message = json.loads(message)
    # print(message)
    table = message.get("table")
    action = message.get("action")
    data = message.get("data")[0]
    if action == "insert":
        # print(data)
        if prev_save_time == None:
            prev_save_time = datetime.now()
            initial_time = datetime.now()
        # print(data)

        if data['symbol'] == "XBTUSD":
            prev_xbt_usd = data['price']
        elif data['symbol'] == "XBTZ21":
            prev_xbt_sub = data['price']

        if datetime.now() - prev_save_time > timedelta(seconds=1):
            save_data()
            prev_save_time = datetime.now()
        if datetime.now() - initial_time > timedelta(minutes=5):
            ws.close()
    else:
        if data['symbol'] == "XBTUSD":
            prev_usd_bid = data['bids'][0][0]
            prev_usd_ask = data['asks'][0][0]
        elif data['symbol'] == "XBTZ21":
            prev_sub_bid = data['bids'][0][0]
            prev_sub_ask = data['asks'][0][0]

def save_data():
    query = RealTimeData.objects.filter(market="bitmex").last()
    print(prev_xbt_sub)
    query.xbt_usd = prev_xbt_usd
    query.xbt_sub = prev_xbt_sub
    query.bid_usd = prev_usd_bid
    query.ask_usd = prev_usd_ask
    query.bid_sub = prev_sub_bid
    query.ask_sub = prev_sub_ask
    query.save()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    ws.send('{"op": "subscribe", "args": ["trade:XBTUSD"]}')
    ws.send('{"op": "subscribe", "args": ["trade:XBTZ21"]}')
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTUSD"]}')
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTZ21"]}')
    

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://www.bitmex.com/realtime",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)

    ws.run_forever()