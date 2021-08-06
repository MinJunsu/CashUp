from django.contrib import admin
from .models import HourData, MinuteData


# Register your models here.
@admin.register(HourData)
class HourDataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'max_price', 'min_price', 'continue_up_down', 'signal', 'volume_rate', 'work_two_1_5', 'work_one_1_0', 'work_one_1_5', ]
    search_fields = ['signal']


@admin.register(MinuteData)
class MinuteDataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'open_price', 'min_price', 'max_price', 'close_price']