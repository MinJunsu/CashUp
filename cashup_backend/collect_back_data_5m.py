import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django

django.setup()

from data.models import HourData, MinuteData, HourSubData, MinuteSubData

# for idx, element in enumerate(reversed(HourData.objects.all())):
#     if idx <= 10000:
#         datetime = element.datetime
#         element.time = f"{str(datetime.day).zfill(2)} {str(datetime.hour).zfill(2)}:{str(datetime.minute).zfill(2)}"
#         element.save()
#     else:
#         break

for idx, element in enumerate(reversed(MinuteData.objects.all())):
    if idx <= 1000:
        datetime = element.datetime
        element.time = f"{str(datetime.day).zfill(2)} {str(datetime.hour).zfill(2)}:{str(datetime.minute).zfill(2)}"
        element.save()
    else:
        break

for idx, element in enumerate(reversed(HourSubData.objects.all())):
    if idx <= 1000:
        datetime = element.datetime
        element.time = f"{str(datetime.day).zfill(2)} {str(datetime.hour).zfill(2)}:{str(datetime.minute).zfill(2)}"
        element.save()
    else:
        break

for idx, element in enumerate(reversed(MinuteSubData.objects.all())):
    if idx <= 1000:
        datetime = element.datetime
        element.time = f"{str(datetime.day).zfill(2)} {str(datetime.hour).zfill(2)}:{str(datetime.minute).zfill(2)}"
        element.save()
    else:
        break
