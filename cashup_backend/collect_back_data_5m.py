import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django
django.setup()

from data.models import MinuteData

import requests
from datetime import timedelta, datetime

start = 0

while True:
    URL = "https://www.bitmex.com/api/v1/trade/bucketed?symbol=XBT&binSize=5m&partial=false&start={}&count=1000&reverse=false".format(
        start)
    request = requests.get(URL).json()
    for data in request:
        datetime = datetime.strptime(data['timestamp'].replace("T", " ")[0:19], "%Y-%m-%d %H:%M:%S") + timedelta(
            hours=9) - timedelta(minutes=5)
        open_price = data['open'] if data['open'] is not None else 0
        high_price = data['high'] if data['high'] is not None else 0
        low_price = data['low'] if data['low'] is not None else 0
        close_price = data['close'] if data['close'] is not None else 0
        volume = data['volume'] if data['volume'] is not None else 0
        obj = MinuteData()
        obj.time = f"{datetime.day} {datetime.hour}:{datetime.minute}"
        obj.min_price = low_price
        obj.max_price = high_price
        obj.open_price = open_price
        obj.close_price = close_price
        obj.volume = volume
        obj.datetime = datetime
        obj.save()

    if len(request) != 1000:
        break

    start += 1000
