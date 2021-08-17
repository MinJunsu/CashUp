import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django
django.setup()

import requests
from datetime import timedelta, datetime
from data.models import HourData

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
prev_signal_up_price = 0
prev_signal_down_price = 0

URL = "https://www.bitmex.com/api/v1/trade/bucketed?symbol=XBT&binSize=1h&partial=true&count=1000&reverse=true"
req = requests.get(URL).json()
req.reverse()
for num_count in range(len(req)):
    data = req[num_count]
    volume_up_dn = ""
    signal = ""
    signal_price = 0
    hour_up_down = ""
    now_work_1_0_1 = ""
    now_work_1_5_1 = ""
    now_work_1_0_2 = ""
    now_work_1_5_2 = ""
    datetime = datetime.strptime(data['timestamp'].replace("T", " ")[0:19], "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
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

    if UD == "U":
        if other_up_dn_list.count("D") > 2:
            if other_up_dn_list.count("D") == 6:
                if prev_up_down == "D" and max(dn_list) == dn_list[0]:
                    if prev_signal_down_price != 0:
                        if prev_signal_down_price < min(up_list):
                            signal = "fD(U)"
                        elif prev_signal_down_price == min(up_list):
                            signal = "fD(0)"
                        else:
                            signal = "fD(D)"
                    prev_signal_down_price = min(up_list)
            else:
                other_up_dn_list.reverse()
                up_list.reverse()
                dn_list.reverse()
                count = 0
                max_price_list = []
                min_price_list = []
                for idx, element in enumerate(other_up_dn_list):
                    if element == "D":
                        count += 1
                        max_price_list.append(dn_list[idx])
                    min_price_list.append(up_list[idx])
                    if count == 3:
                        break
                if prev_up_down == "D" and max(max_price_list) == max_price_list[2]:
                    if prev_signal_down_price != 0:
                        if prev_signal_down_price < min(min_price_list):
                            signal = "fD(U)"
                        elif prev_signal_down_price == min(min_price_list):
                            signal = "fD(0)"
                        else:
                            signal = "fD(D)"
                    prev_signal_down_price = min(min_price_list)
                other_up_dn_list.reverse()
                up_list.reverse()
                dn_list.reverse()

    if UD == "D":
        if other_up_dn_list.count("U") > 2:
            if other_up_dn_list.count("U") == 6:
                if prev_up_down == "U" and min(up_list) == up_list[0]:
                    if prev_signal_up_price < max(dn_list):
                        signal = "fU(U)"
                    elif prev_signal_up_price == max(dn_list):
                        signal = "fU(0)"
                    else:
                        signal = "fU(D)"
                    prev_signal_down_price = max(dn_list)
            else:
                other_up_dn_list.reverse()
                up_list.reverse()
                dn_list.reverse()
                count = 0
                max_price_list = []
                min_price_list = []
                print(datetime)
                for idx, element in enumerate(other_up_dn_list):
                    print(idx, element)
                    if element == "U":
                        count += 1
                        min_price_list.append(up_list[idx])
                    max_price_list.append(dn_list[idx])
                    if count == 3:
                        break
                if prev_up_down == "U" and min(min_price_list) == min_price_list[2]:
                    if prev_signal_down_price != 0:
                        if prev_signal_down_price < max(max_price_list):
                            signal = "fU(U)"
                        elif prev_signal_down_price == max(max_price_list):
                            signal = "fU(0)"
                        else:
                            signal = "fU(D)"
                    prev_signal_down_price = max(max_price_list)
                other_up_dn_list.reverse()
                up_list.reverse()
                dn_list.reverse()
    if len(dn_list) > 5:
        dn_list.pop(0)
    dn_list.append(high_price)

    if len(up_list) > 5:
        up_list.pop(0)
    up_list.append(low_price)

    if len(other_up_dn_list) > 5:
        other_up_dn_list.pop(0)
    other_up_dn_list.append(UD)

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

    if num_count > 990:
        print("실행")
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
            'up_down': UD,
            'continue_up_down': continue_up_down,
            'hour_up_down': hour_up_down,
            'signal': signal,
            'work_two_1_0': now_work_1_0_1,
            'work_two_1_5': now_work_1_5_1,
            'work_one_1_0': now_work_1_0_2,
            'work_one_1_5': now_work_1_5_2   
        }
        HourData.objects.update_or_create(datetime=datetime, defaults=default)

    prev_up_down = UD