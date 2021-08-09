from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import simulate
import json
from django.core.serializers.json import DjangoJSONEncoder

@csrf_exempt
def index(request):
    Simulation = simulate.Simulate()
    if request.method == "POST":
        data = json.loads(request.body)
        start_time = data['startTime']
        end_time = data['endTime']
        buy_rate = int(data['buyRate'])
        sell_rate = int(data['sellRate'])
        search_amount = 800
        trade_limit = 800
        Simulation.set_default(buy_rate=buy_rate, sell_rate=sell_rate, search_amount=search_amount, trade_limit=trade_limit)
        if data['version'] == '1':
            Simulation.simulate(data['type'], start_time, end_time)
        elif data['version'] == '2':
            Simulation.simulate2(data['type'], start_time, end_time)
        elif data['version'] == '3':
            Simulation.simulate3(data['type'], start_time, end_time)

        result = {
            'data': Simulation.long_result_list,
            'result': Simulation.long_result_dict
        }

        return HttpResponse(
            json.dumps(result, cls=DjangoJSONEncoder)
        )