from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from .models import TradeResult, TradeSetting
from .serializer import TradeResultModelSerializer
from rest_framework.response import Response

# Create your views here.
class TradeResultAPIView(APIView):
    def get(self, request):
        version = int(request.GET.get('version', '1'))
        accounts = 0
        if version == 1:
            accounts = 2
        elif version == 2:
            accounts = 3
        elif version == 3:
            accounts = 4
        long_query = TradeResult.objects.filter(Q(position=True), Q(user=accounts), ~Q(buy_order_time=None), Q(sell_time=None))
        long_finished_query = TradeResult.objects.filter(Q(position=True), Q(user=accounts), ~Q(sell_time=None))
        short_query = TradeResult.objects.filter(Q(position=False), Q(user=accounts), ~Q(buy_order_time=None), Q(sell_time=None))
        short_finished_query = TradeResult.objects.filter(Q(position=False), Q(user=accounts), ~Q(sell_time=None))
        long_trade = TradeResultModelSerializer(long_query, many=True)
        long_finished_trade = TradeResultModelSerializer(long_finished_query, many=True)
        short_trade = TradeResultModelSerializer(short_query, many=True)
        short_finished_trade = TradeResultModelSerializer(short_finished_query, many=True)
        return Response({
            "long": long_trade.data,
            'long_finished': long_finished_trade.data,
            'short': short_trade.data,
            'short_finished': short_finished_trade.data
        })
