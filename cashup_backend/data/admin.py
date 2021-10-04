from django.contrib import admin
from .models import RealTimeData, HourData, MinuteData, HourSubData, MinuteSubData, UpFlow, DownFlow


# Register your models here.
@admin.register(RealTimeData)
class RealTimeDataAdmin(admin.ModelAdmin):
    list_display = ['market', 'updated_time', 'xbt_usd', 'xbt_sub', 'bid_usd', 'ask_usd', 'bid_sub', 'ask_sub']

@admin.register(HourData)
class HourDataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'open_price', 'min_price', 'max_price', 'close_price', 'up_down', 'continue_up_down', 'volume_rate', 'signal', 'work_one_1_0']
    search_fields = ['signal']


@admin.register(MinuteData)
class MinuteDataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'open_price', 'min_price', 'max_price', 'close_price', 'up_down', 'flow', 'signal']

@admin.register(HourSubData)
class U21HourDataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'open_price', 'min_price', 'max_price', 'close_price', 'up_down', 'continue_up_down', 'volume_rate', 'signal', 'work_one_1_0']
    search_fields = ['signal']


@admin.register(MinuteSubData)
class U21MinuteDataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'open_price', 'min_price', 'max_price', 'close_price', 'up_down', 'flow', 'signal']


@admin.register(UpFlow)
class UpFlowAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'base_price', 'flow', 'flow_confirm', 'flow_trade']


@admin.register(DownFlow)
class DownFlowAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'base_price', 'flow', 'flow_confirm', 'flow_trade']