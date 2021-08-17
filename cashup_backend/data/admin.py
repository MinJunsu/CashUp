from django.contrib import admin
from .models import HourData, MinuteData, UpFlow, DownFlow


# Register your models here.
@admin.register(HourData)
class HourDataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'open_price', 'min_price', 'max_price', 'close_price', 'up_down', 'continue_up_down', 'volume_rate', 'signal', 'work_one_1_0']
    search_fields = ['signal']


@admin.register(MinuteData)
class MinuteDataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'open_price', 'min_price', 'max_price', 'close_price', 'flow', 'signal']

@admin.register(UpFlow)
class UpFlowAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'base_price', 'up_flow', 'up_flow_confirm', 'up_flow_trade']

@admin.register(DownFlow)
class DownFlowAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'base_price', 'down_flow', 'down_flow_confirm', 'down_flow_trade']