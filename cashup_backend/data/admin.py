from django.contrib import admin
from .models import HourData, MinuteData, HourSubData, MinuteSubData

# Register your models here.


@admin.register(HourData)
class HourDataAdmin(admin.ModelAdmin):
    pass


@admin.register(MinuteData)
class MinuteDataAdmin(admin.ModelAdmin):
    pass


@admin.register(HourSubData)
class HourSubDataAdmin(admin.ModelAdmin):
    pass


@admin.register(MinuteSubData)
class MinuteSubDataAdmin(admin.ModelAdmin):
    pass
