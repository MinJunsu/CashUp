from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from django.core.serializers.json import DjangoJSONEncoder
from .models import HourData
import json
# Create your views here.


class ProgressbarAPIView(APIView):
    def get(self, request):
        from datetime import timedelta, datetime
        now_price = HourData.objects.all().order_by('-datetime')[0].close_price
        downSignal = HourData.objects.all().order_by('-datetime').filter(signal='fD(D)')[0].datetime
        upSignal = HourData.objects.all().order_by('-datetime').filter(signal='fU(U)')[0].datetime
        upMaxPrice, upMinPrice = getPercent(upSignal)
        downMaxPrice, downMinPrice = getPercent(downSignal)
        return HttpResponse(content=json.dumps({
            'now_price': now_price,
            'up_base_time': upSignal,
            'down_base_time': downSignal,
            'up_base_max_price': upMaxPrice,
            'up_base_min_price': upMinPrice,
            'down_base_max_price': downMaxPrice,
            'down_base_min_price': downMinPrice
        }, cls=DjangoJSONEncoder))
        
def getPercent(time):
    print(time)
    from datetime import datetime, timedelta
    max_list = [0]
    min_list = []
    for element in HourData.objects.filter(datetime__range=(time - timedelta(hours=6), time)):
        print(element.up_down)
        if element.up_down == "U":
            min_list.append(element.min_price)
    
    flag = False
    for element in HourData.objects.filter(datetime__range=(time, datetime.now())):
        if element.up_down == "D":
            flag = True
        if flag:
            max_list.append(element.max_price)
    
    return max(max_list), min(min_list)
    