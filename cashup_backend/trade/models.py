from django.conf import settings
from django.db import models


# Create your models here.
class TradeSetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_trade = models.BooleanField(default=True)
    real_trade = models.BooleanField(default=False)
    version = models.IntegerField(default=1)
    buy_rate_option = models.IntegerField(default=10)
    sell_rate_option = models.IntegerField(default=10)


class TradeResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.BooleanField(default=False)
    signal_time = models.DateTimeField(null=True, blank=True)
    buy_order_time = models.DateTimeField(null=True, blank=True)
    buy_time = models.DateTimeField(null=True, blank=True)
    amount = models.IntegerField(default=100)
    buy_price = models.FloatField(default=0)
    version = models.IntegerField(default=1)
    sell_order_time = models.DateTimeField(null=True, blank=True)
    sell_time = models.DateTimeField(null=True, blank=True)
    sell_price = models.FloatField(default=0)
    max_rate = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    min_rate = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    earning_rate = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    def calculate_earning_rate(self, now_price):
        if self.position:
            if self.buy_price > now_price:
                self.earning_rate = round(-(((self.buy_price - now_price) / self.buy_price) * 100), 4) * 100
            else:
                self.earning_rate = round(((now_price / self.buy_price) - 1) * 100, 4) * 100
            if self.earning_rate > self.max_rate:
                self.max_rate = self.earning_rate
            if self.min_rate > self.earning_rate:
                self.min_rate = self.earning_rate
        else:
            if self.buy_price > now_price:
                self.earning_rate = round(((self.buy_price - now_price) / self.buy_price) * 100, 4) * 100
            else:
                self.earning_rate = round(-((now_price / self.buy_price) - 1) * 100, 4) * 100
            if self.earning_rate > self.max_rate:
                self.max_rate = self.earning_rate
            if self.min_rate > self.earning_rate:
                self.min_rate = self.earning_rate
