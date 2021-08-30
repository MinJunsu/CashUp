from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers.json import DjangoJSONEncoder

from datetime import datetime, timedelta
import json

from .models import HourData, MinuteData, UpFlow, DownFlow
from .serializer import HourDataModelSerializer, MinuteDataModelSerializer, UpFlowModelSerializer, DownFlowModelSerializer

# Create your views here.
class HourAPIView(APIView):
    def get(self, request):
        term = int(request.GET.get('term', '14'))
        hour_query = HourData.objects.filter(datetime__gt=datetime.now() - timedelta(days=term)).order_by('-id')
        serializer = HourDataModelSerializer(hour_query, many=True)
        return Response({
            "candle": serializer.data
        })

class MinuteAPIView(APIView):
    def get(self, request):
        term = int(request.GET.get('term', '14'))
        minute_query = MinuteData.objects.filter(datetime__gt=datetime.now() - timedelta(days=term)).order_by('-id')
        serializer = MinuteDataModelSerializer(minute_query, many=True)
        return Response({
            "candle": serializer.data
        })

class UpFlowAPIView(APIView):
    def get(self, request):
        term = int(request.GET.get('term', '14'))
        upflow_query = UpFlow.objects.filter(datetime__gt=datetime.now() - timedelta(days=term)).order_by('-id')
        serializer = UpFlowModelSerializer(upflow_query, many=True)
        return Response({
            "flow": serializer.data
        })

class DownFlowAPIView(APIView):
    def get(self, request):
        term = int(request.GET.get('term', '14'))
        downflow_query = DownFlow.objects.filter(datetime__gt=datetime.now() - timedelta(days=term)).order_by('-id')
        serializer = DownFlowModelSerializer(downflow_query, many=True)
        return Response({
            "flow": serializer.data
        })

class FlagAPIView(APIView):
    def get(self, request):
        hour_flag, minute_flag, upflow_flag, downflow_flag = True, True, False, False
        if datetime.now() - UpFlow.objects.last().datetime < timedelta(minutes=5):
            upflow_flag = True
        if datetime.now() - DownFlow.objects.last().datetime < timedelta(minutes=5):
            downflow_flag = True
        return HttpResponse(json.dumps({
            'hour_flag': hour_flag,
            'minute_flag': minute_flag,
            'upflow_flag': upflow_flag,
            'downflow_flag': downflow_flag
        }, cls=DjangoJSONEncoder))

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
    