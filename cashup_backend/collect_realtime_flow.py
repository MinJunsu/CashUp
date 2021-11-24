import django
from datetime import timedelta, datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

django.setup()

from data.models import UpFlow, DownFlow

up_flow_list = UpFlow.objects.filter(id__gte=(UpFlow.objects.last().id) - 300)
down_flow_list = DownFlow.objects.filter(id__gte=(DownFlow.objects.last().id) - 300)
up_flow_up_down_list = []
up_flow_confirm_list = []
up_flow_element_list = []
down_flow_up_down_list = []
down_flow_confirm_list = []
down_flow_element_list = []

for element in up_flow_list:
    if len(up_flow_up_down_list) > 4:
        up_flow_up_down_list.pop(0)
        up_flow_confirm_list.pop(0)
        up_flow_element_list.pop(0)
    up_flow_up_down_list.append(element.flow)
    up_flow_confirm_list.append(element.flow_confirm)
    up_flow_element_list.append(element)

    if len(up_flow_up_down_list) > 4:
        # Version 4
        if up_flow_up_down_list.count("UP") == 5:
            element.flow_trade = "B#4"
            element.save()
        # Version 2
        if up_flow_confirm_list[4] is None and up_flow_confirm_list[3] == "DN" and up_flow_confirm_list[2] is None:
            up_flow_element_list[3].flow_trade = "B#2"
            up_flow_element_list[3].save()
        # Version 1
        if up_flow_confirm_list[3] == "UP" and up_flow_confirm_list[4] is None:
            up_flow_element_list[3].flow_trade = "S#1"
            up_flow_element_list[3].save()
        # Version 3
        if up_flow_up_down_list[3] == "UP" and up_flow_up_down_list[4] == "UP" and up_flow_confirm_list[4] != "UP":
            element.up_flow_trade = "S#3"
            element.save()

for element in down_flow_list:
    if len(down_flow_up_down_list) > 4:
        down_flow_up_down_list.pop(0)
        down_flow_confirm_list.pop(0)
        down_flow_element_list.pop(0)
    down_flow_up_down_list.append(element.flow)
    down_flow_confirm_list.append(element.flow_confirm)
    down_flow_element_list.append(element)

    if len(down_flow_up_down_list) > 4:
        # Version 4
        if down_flow_up_down_list.count("DN") == 5:
            element.flow_trade = "S#4"
            element.save()
        # Version 2
        if down_flow_confirm_list[4] is None and down_flow_confirm_list[3] == "UP" and down_flow_confirm_list[2] is None:
            down_flow_element_list[3].flow_trade = "S#2"
            down_flow_element_list[3].save()
        # Version 1
        if down_flow_confirm_list[3] == "DN" and down_flow_confirm_list[4] is None:
            down_flow_element_list[3].flow_trade = "B#1"
            down_flow_element_list[3].save()
        # Version 3
        if down_flow_up_down_list[3] == "DN" and down_flow_up_down_list[4] == "DN" and down_flow_confirm_list[4] != "DN":
            element.flow_trade = "B#3"
            element.save()
