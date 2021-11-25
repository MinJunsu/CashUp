from django.db import models


# Create your models here.
class Data(models.Model):
    time = models.CharField(max_length=10, null=True)
    min_price = models.FloatField()
    max_price = models.FloatField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()
    datetime = models.DateTimeField()

    class Meta:
        abstract = True


class RealTimeData(models.Model):
    market = models.CharField(max_length=10)
    updated_time = models.DateTimeField(auto_now=True)
    xbt_usd = models.FloatField(verbose_name='XBTUSD')
    xbt_sub = models.FloatField(verbose_name='XBTSUB')
    bid_usd = models.FloatField(verbose_name='BIDUSD')
    ask_usd = models.FloatField(verbose_name='ASKUSD')
    bid_sub = models.FloatField(verbose_name='BIDSUB')
    ask_sub = models.FloatField(verbose_name='ASKSUB')


class HourData(Data):
    
    def __str__(self):
        return str(self.datetime)


class HourSubData(Data):

    def __str__(self):
        return str(self.datetime)


class MinuteSubData(Data):
    real = models.CharField(max_length=4, default='')

    def __str__(self):
        return str(self.datetime)


class MinuteData(Data):
    real = models.CharField(max_length=4, default='')

    def __str__(self):
        return str(self.datetime)
