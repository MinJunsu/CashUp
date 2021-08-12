from django.contrib import admin
from .models import TradeSetting, TradeResult


# Register your models here.
@admin.register(TradeSetting)
class TradeSettingAdmin(admin.ModelAdmin):
    list_display = ['user', 'test_trade', 'real_trade', 'version', 'buy_rate_option', 'sell_rate_option']


@admin.register(TradeResult)
class TradeResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'version', 'buy_order_time', 'buy_time', 'amount', 'buy_price', 'sell_order_time', 'sell_time', 'sell_price', 'max_rate', 'min_rate', 'earning_rate']