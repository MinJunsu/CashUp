from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.core.serializers.json import DjangoJSONEncoder

from datetime import timedelta, datetime
import json

from .models import HourData, MinuteData, UpFlow, DownFlow
from .serializer import HourDataModelSerializer, MinuteDataModelSerializer, UpFlowModelSerializer, DownFlowModelSerializer

# Create your views here.
class DataAPIView(APIView):
    def get(self, request):
        term = int(request.GET.get('term', '14'))
        hour_query = HourData.objects.filter(datetime__gt=datetime.now() - timedelta(days=term)).order_by('-id')
        minute_query = MinuteData.objects.filter(datetime__gt=datetime.now() - timedelta(days=term)).order_by('-id')
        up_flow_query = UpFlow.objects.filter(datetime__gt=datetime.now() - timedelta(days=term)).order_by('-id')
        down_flow_query = DownFlow.objects.filter(datetime__gt=datetime.now() - timedelta(days=term)).order_by('-id')
        hour_serializer = HourDataModelSerializer(hour_query, many=True)
        minute_serializer = MinuteDataModelSerializer(minute_query, many=True)
        up_flow_serializer = UpFlowModelSerializer(up_flow_query, many=True)
        down_flow_serializer = DownFlowModelSerializer(down_flow_query, many=True)
        return Response({
            "hour": hour_serializer.data,
            "minute": minute_serializer.data,
            "up_flow": up_flow_serializer.data,
            "down_flow": down_flow_serializer.data
        })


class ProgressbarAPIView(APIView):
    def get(self, request):
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
    