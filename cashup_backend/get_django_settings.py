import os
import django
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

django.setup()

from data.models import MinuteData, HourData

if time.localtime().tm_min % 5 != 0:
    exit