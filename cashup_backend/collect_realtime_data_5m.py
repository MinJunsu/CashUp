import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django
django.setup()

import requests
from datetime import timedelta, datetime
from data.models import MinuteData


URL = "https://www.bitmex.com/api/v1/trade/bucketed?symbol=XBT&binSize=5m&partial=true&count=5&reverse=true"
request = requests.get(URL).json()
for idx, data in enumerate(reversed(request)):
    datetime = datetime.strptime(data['timestamp'].replace("T", " ")[0:19], "%Y-%m-%d %H:%M:%S") + timedelta(
        hours=9) - timedelta(minutes=5)
    open_price = data['open'] if data['open'] is not None else 0
    high_price = data['high'] if data['high'] is not None else 0
    low_price = data['low'] if data['low'] is not None else 0
    close_price = data['close'] if data['close'] is not None else 0
    volume = data['volume'] if data['volume'] is not None else 0
    if idx >= 3:
        MinuteData.objects.update_or_create(datetime=datetime, defaults={
            'time': f"{str(datetime.day).zfill(2)} {str(datetime.hour).zfill(2)}:{str(datetime.minute).zfill(2)}",
            'open_price': open_price,
            'min_price': low_price,
            'max_price': high_price,
            'close_price': close_price,
            'volume': volume,
            'real': 'real'
        })
    else:
        MinuteData.objects.update_or_create(datetime=datetime, defaults={
            'time': f"{str(datetime.day).zfill(2)} {str(datetime.hour).zfill(2)}:{str(datetime.minute).zfill(2)}",
            'open_price': open_price,
            'min_price': low_price,
            'max_price': high_price,
            'close_price': close_price,
            'volume': volume,
            'real': ''
        })
