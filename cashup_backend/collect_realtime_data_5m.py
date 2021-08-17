import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django
django.setup()

import requests
from datetime import timedelta, datetime
from data.models import MinuteData, HourData, UpFlow, DownFlow

up_dn_list = []
last_data = []
dn_list = []
up_list = []
new_dn_list = []
new_up_list = []
other_up_dn_list = []

continue_up_down = "D0"
prev_up_down = "S"
work_1_0_1 = "S"
work_1_5_1 = "S"
work_1_0_2 = "S"
work_1_5_2 = "S"
last_time_1_0_1 = datetime.now()
last_time_1_5_1 = datetime.now()
last_time_1_0_2 = datetime.now()
last_time_1_5_2 = datetime.now()

last_dn, last_up = "", ""

max_price, min_price = 0, 0
work_up_high, work_dn_low = 1000000, 0
volume = 0
prev_low = 0
prev_high = 100000
start = 0
last_up = 0
last_dn = 0
volume_up_dn = ""
hour_up_down = ""
prev_signal_down_price = 0
prev_signal_up_price = 0

base_price = 0
flow_base_price = 0
prev_signal = ""
flow_list = []
flow_element_list = []
prev_down_flow = 0
prev_up_flow = 0
down_flow = ['DN', 'DN', 'UP', 'UP']
up_flow = ['UP', 'UP', 'DN', 'DN']
down_flow_list = []
up_flow_list = []
last_down_flow_time = ""
last_up_flow_time = ""
down_flow_element_list = []
down_flow_confirm_list = []
up_flow_element_list = []
up_flow_confirm_list = []

URL = "https://www.bitmex.com/api/v1/trade/bucketed?symbol=XBT&binSize=5m&partial=true&count=1000&reverse=true"
req = requests.get(URL).json()
req.reverse()
for count in range(len(req)):
    data = req[count]
    print(data)
    volume_up_dn = ""
    signal = ""
    signal_price = 0
    hour_up_down = ""
    now_work_1_0_1 = ""
    now_work_1_5_1 = ""
    now_work_1_0_2 = ""
    now_work_1_5_2 = ""
    datetime = datetime.strptime(data['timestamp'].replace("T", " ")[0:19], "%Y-%m-%d %H:%M:%S") + timedelta(hours=9) - timedelta(minutes=5)
    open_price = data['open']
    high_price = data['high']
    low_price = data['low']
    close_price = data['close']
    avg_price = (high_price + low_price) / 2

    if volume != 0:
        volume_rate = data['volume'] / volume
    else:
        volume_rate = 0

    volume = data['volume']

    flag = False

    if open_price > close_price:
        UD = "D"

    elif open_price < close_price:
        UD = "U"

    else:
        UD = "S"

    if len(last_data) > 3:
        last_data.pop(0)
        volume_bigger_count = 0
        volume_smaller_count = 0

        for i in last_data:
            if i[2] < volume:
                volume_bigger_count += 1

            if i[2] > volume:
                volume_smaller_count += 1

        if volume_bigger_count == 3:
            volume_up_dn = "UP"

        if volume_smaller_count == 3:
            volume_up_dn = "DN"

    last_data.append([low_price, high_price, volume])

    if continue_up_down[0] == "U":
        if UD == "U":
            continue_up_down = "U" + str(int(continue_up_down[1:]) + 1)
        elif UD == "D":
            continue_up_down = "D1"
    else:
        if UD == "U":
            continue_up_down = "U1"
        elif UD == "D":
            continue_up_down = "D" + str(int(continue_up_down[1:]) + 1)

    if len(up_dn_list) > 3:
        up_dn_list.pop(0)
    up_dn_list.append(UD)

    if up_dn_list.count("U") > 2:
        if high_price >= last_up:
            hour_up_down = "UP(U)"
        else:
            hour_up_down = "UP(D)"
        last_up = high_price

    if up_dn_list.count("D") > 2:
        if low_price >= last_dn:
            hour_up_down = "DN(U)"
        else:
            hour_up_down = "DN(D)"
        last_dn = low_price

    if len(dn_list) > 5:
        dn_list.pop(0)
    dn_list.append(high_price)

    if len(up_list) > 5:
        up_list.pop(0)
    up_list.append(low_price)

    if len(other_up_dn_list) > 5:
        other_up_dn_list.pop(0)
    other_up_dn_list.append(UD)

    if UD == "U":
        if other_up_dn_list.count("D") > 2:
            if other_up_dn_list.count("D") == 6:
                if prev_up_down == "D" and max(dn_list) == dn_list[0]:
                    if prev_signal_down_price != 0:
                        if prev_signal_down_price <= dn_list[0]:
                            signal = "fD(U)"
                        else:
                            signal = "fD(D)"
                        signal_price = min(dn_list)
                    prev_signal_down_price = dn_list[0]
            else:
                if prev_up_down == "D" and max(new_dn_list) == new_dn_list[0]:
                    if prev_signal_down_price <= new_dn_list[0]:
                        signal = "fD(U)"
                    else:
                        signal = "fD(D)"
                    signal_price = min(new_dn_list)
                    prev_signal_down_price = dn_list[0]
        if len(new_up_list) > 2:
            new_up_list.pop(0)
        new_up_list.append(low_price)

    if UD == "D":
        if other_up_dn_list.count("U") > 2:
            if other_up_dn_list.count("U") == 6:
                if prev_up_down == "U" and min(up_list) == up_list[0]:
                    if prev_signal_up_price <= up_list[0]:
                        signal = "fU(U)"
                    else:
                        signal = "fU(D)"
                    signal_price = max(up_list)
                    prev_signal_down_price = dn_list[0]
            else:
                if prev_up_down == "U" and min(new_up_list) == new_up_list[0]:
                    if prev_signal_up_price != 0:
                        if prev_signal_up_price <= new_up_list[0]:
                            signal = "fU(U)"
                        else:
                            signal = "fU(D)"
                        signal_price = max(new_up_list)
                    prev_signal_up_price = up_list[0]
        if len(new_dn_list) > 2:
            new_dn_list.pop(0)
        new_dn_list.append(high_price)

    if volume_up_dn == "UP":
        if (max_price < high_price) and (volume_rate > 1):
            if work_1_0_1[0] == "U":
                if datetime == last_time_1_0_1 + timedelta(hours=1):
                    continue_flag_1_0_1 = True
                else:
                    work_1_0_1 = "U" + str(int(work_1_0_1[1:]) + 1)
            else:
                work_1_0_1 = "U1"

            now_work_1_0_1 = work_1_0_1
            last_time_1_0_1 = datetime

        if (min_price > low_price) and (volume_rate > 1):
            if work_1_0_1[0] == "D":
                if datetime == last_time_1_0_1 + timedelta(hours=1):
                    continue_flag_1_0 = True
                else:
                    work_1_0_1 = "D" + str(int(work_1_0_1[1:]) + 1)

            else:
                work_1_0_1 = "D1"

            now_work_1_0_1 = work_1_0_1
            last_time_1_0_1 = datetime

        if (max_price < high_price) and (volume_rate > 1.5):
            if work_1_5_1[0] == "U":
                if datetime == last_time_1_5_1 + timedelta(hours=1):
                    continue_flag_1_5_1 = True
                else:
                    work_1_5_1 = "U" + str(int(work_1_5_1[1:]) + 1)
            else:
                work_1_5_1 = "U1"

            now_work_1_5_1 = work_1_5_1
            last_time_1_5_1 = datetime

        if (min_price > low_price) and (volume_rate > 1.5):
            if work_1_5_1[0] == "D":
                if datetime == last_time_1_5_1 + timedelta(hours=1):
                    pass
                else:
                    work_1_5_1 = "D" + str(int(work_1_5_1[1:]) + 1)

            else:
                work_1_5_1 = "D1"

            now_work_1_5_1 = work_1_5_1
            last_time_1_5_1 = datetime

        if (max_price < high_price and min_price < low_price) and (volume_rate > 1):
            if work_1_0_2[0] == "U":
                if datetime == last_time_1_0_2 + timedelta(hours=1):
                    pass
                else:
                    work_1_0_2 = "U" + str(int(work_1_0_2[1:]) + 1)
            else:
                work_1_0_2 = "U1"

            now_work_1_0_2 = work_1_0_2
            last_time_1_0_2 = datetime

        if (min_price > low_price and max_price > high_price) and (volume_rate > 1):
            if work_1_0_2[0] == "D":
                if datetime == last_time_1_0_2 + timedelta(hours=1):
                    pass
                else:
                    work_1_0_2 = "D" + str(int(work_1_0_2[1:]) + 1)

            else:
                work_1_0_2 = "D1"

            now_work_1_0_2 = work_1_0_2
            last_time_1_0_2 = datetime

        if (max_price < high_price and min_price < low_price) and (volume_rate > 1.5):
            if work_1_5_2[0] == "U":
                if datetime == last_time_1_5_2 + timedelta(hours=1):
                    pass
                else:
                    work_1_5_2 = "U" + str(int(work_1_5_2[1:]) + 1)
            else:
                work_1_5_2 = "U1"

            now_work_1_5_2 = work_1_5_2
            last_time_1_5_2 = datetime

        if (min_price > low_price and max_price > high_price) and (volume_rate > 1.5):
            if work_1_5_2[0] == "D":
                if datetime == last_time_1_5_1 + timedelta(hours=1):
                    pass
                else:
                    work_1_5_2 = "D" + str(int(work_1_5_2[1:]) + 1)

            else:
                work_1_5_2 = "D1"

            now_work_1_5_2 = work_1_5_2
            last_time_1_5_2 = datetime

        max_price, min_price = high_price, low_price

    if now_work_1_0_1 != "":
        now_work_1_0_1 = "w" + now_work_1_0_1

    if now_work_1_5_1 != "":
        now_work_1_5_1 = "w" + now_work_1_5_1

    if now_work_1_0_2 != "":
        now_work_1_0_2 = "w" + now_work_1_0_2

    if now_work_1_5_2 != "":
        now_work_1_5_2 = "w" + now_work_1_5_2

    flow = ""
    if flow_base_price != 0:
        if prev_signal == "fU(D)":
            if high_price > flow_base_price:
                flow = "UP"
            else:
                flow = "DN"
        if prev_signal == "fD(U)":
            if low_price > flow_base_price:
                flow = "UP"
            else:
                flow = "DN"

    if signal == "fU(D)":
        flow_base_price = high_price
        prev_signal = signal

    if signal == "fD(U)":
        flow_base_price = low_price
        prev_signal = signal

    if flow != "":
        if len(flow_list) > 3:
            flow_list.pop(0)
            flow_element_list.pop(0)
        flow_list.append(flow)
        flow_element_list.append({
            'datetime': datetime,
            'min_price': low_price,
            'max_price': high_price
        })

    flow_element = None

    if flow_list == down_flow:
        if prev_down_flow != 0:
            flow_element = DownFlow()
            flow_element.datetime = flow_element_list[1]['datetime']
            flow_element.base_price = flow_element_list[1]['max_price']
            if prev_down_flow < flow_element_list[1]['max_price']:
                flow_element.down_flow = "UP"
            else:
                flow_element.down_flow = "DN"
            if len(down_flow_list) > 4:
                down_flow_list.pop(0)
            down_flow_list.append(flow_element.down_flow)

            if len(down_flow_list) > 4:
                if down_flow_list.count("UP") > 3:
                    flow_element.down_flow_confirm = "UP"

                if down_flow_list.count("DN") > 3:
                    flow_element.down_flow_confirm = "DN"

                if down_flow_list.count("UP") == 5:
                    flow_element.down_flow_trade("B#4")

        prev_down_flow = flow_element_list[1]['max_price']

    if flow_list == up_flow:
        if prev_up_flow != 0:
            flow_element = UpFlow()
            flow_element.datetime = flow_element_list[1]['datetime']
            flow_element.base_price = flow_element_list[1]['min_price']
            if prev_up_flow < flow_element_list[1]['min_price']:
                flow_element.up_flow = "UP"
            else:
                flow_element.up_flow = "DN"

            if len(up_flow_list) > 4:
                up_flow_list.pop(0)
            up_flow_list.append(flow_element.up_flow)

            if len(up_flow_list) > 4:
                if up_flow_list.count("UP") > 3:
                    flow_element.up_flow_confirm = "UP"

                if up_flow_list.count("DN") > 3:
                    flow_element.up_flow_confirm = "DN"

                if up_flow_list.count("DN") == 5:
                    flow_element.up_flow_trade("S#4")

        prev_up_flow = flow_element_list[1]['min_price']

    if len(flow_element_list) > 3:
        if flow_element:
            flag = False
            if type(flow_element) == UpFlow:
                flag = True

            if not flag and flow_element.down_flow_confirm == "UP":
                last_down_flow_time = flow_element_list[1]['datetime']

            if flag and flow_element.up_flow_confirm == "DN":
                last_up_dlow_time = flow_element_list[1]['datetime']

            if not flag and flow_element.down_flow:
                if last_down_flow_time != "":
                    if flow_element_list[1]['datetime'] - last_down_flow_time > timedelta(hours=2):
                        if HourData.objects.filter(datetime__range=[last_down_flow_time,
                                                                    flow_element_list[1]['datetime'] - timedelta(
                                                                            hours=1)], up_down='U').values(
                                'up_down').count() > 1:
                            flow_element.down_flow_trade = "S#1"
                            last_down_flow_time = ""

                elif down_flow_list[-2:] == ['UP', 'UP']:
                    flow_element.down_flow_trade = "S#2"

                if len(down_flow_element_list) > 1:
                    down_flow_element_list.pop(0)
                down_flow_element_list.append(flow_element)

                if len(down_flow_element_list) > 1:
                    if down_flow_confirm_list[0].down_flow_confirm is None and flow_element.down_flow_confirm == "DN":
                        flow_element.down_flow_trade = "B#2"

            if flag and flow_element.up_flow:
                if last_up_flow_time != "":
                    if flow_element_list[1]['datetime'] - last_up_flow_time > timedelta(hours=2):
                        if HourData.objects.filter(datetime__range=[last_up_flow_time,
                                                                    flow_element_list[1]['datetime'] - timedelta(
                                                                            hours=1)], up_down='D').values(
                                'up_down').count() > 1:
                            flow_element.up_flow_trade = "B#1"
                            last_up_flow_time = ""

                elif up_flow_list[-2:] == ['DN', 'DN']:
                    flow_element.up_flow_trade = "B#2"

                if len(up_flow_element_list) > 1:
                    up_flow_element_list.pop(0)
                up_flow_element_list.append(flow_element)

                if len(up_flow_element_list) > 1:
                    if up_flow_element_list[0].up_flow_confirm is None and flow_element.up_flow_confirm == "UP":
                        flow_element.down_flow_trade = "S#2"

    if flow_element:
        if type(flow_element) == UpFlow:
            default = {
                'datetime': flow_element.datetime,
                'base_price': flow_element.base_price,
                'up_flow': flow_element.up_flow,
                'up_flow_confirm': flow_element.up_flow_confirm,
                'up_flow_trade': flow_element.up_flow_trade
            }
            UpFlow.objects.update_or_create(datetime=flow_element.datetime, defaults=default)
        else:
            default = {
                'datetime': flow_element.datetime,
                'base_price': flow_element.base_price,
                'down_flow': flow_element.down_flow,
                'down_flow_confirm': flow_element.down_flow_confirm,
                'down_flow_trade': flow_element.down_flow_trade
            }
            DownFlow.objects.update_or_create(datetime=flow_element.datetime, defaults=default)

    if count > 980:
        default = {
            'datetime': datetime,
            'open_price': open_price,
            'min_price': low_price,
            'max_price': high_price,
            'close_price': close_price,
            'avg_price': avg_price,
            'volume': volume,
            'volume_rate': volume_rate,
            'volume_up_dn': volume_up_dn,
            'flow': flow,
            'up_down': UD,
            'continue_up_down': continue_up_down,
            'hour_up_down': hour_up_down,
            'signal': signal,
            'signal_price': signal_price,
            'work_two_1_0': now_work_1_0_1,
            'work_two_1_5': now_work_1_5_1,
            'work_one_1_0': now_work_1_0_2,
            'work_one_1_5': now_work_1_5_2   
        }
        MinuteData.objects.update_or_create(datetime=datetime, defaults=default)

    prev_up_down = UD