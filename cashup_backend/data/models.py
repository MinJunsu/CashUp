from django.db import models


# Create your models here.
class HourData(models.Model):
    datetime = models.DateTimeField(verbose_name='시간')
    open_price = models.FloatField(verbose_name='시가')
    min_price = models.FloatField(verbose_name='저가')
    max_price = models.FloatField(verbose_name='고가')
    close_price = models.FloatField(verbose_name='종가')
    avg_price = models.FloatField(verbose_name='평균')
    volume = models.BigIntegerField(verbose_name='거래량')
    volume_rate = models.FloatField(verbose_name='거래량 비')
    volume_up_dn = models.CharField(max_length=2, null=True, verbose_name="거래량 UP/DN")
    up_down = models.CharField(max_length=2, verbose_name='UD')
    continue_up_down = models.CharField(max_length=3, verbose_name='연속 UD')
    hour_up_down = models.CharField(max_length=6, verbose_name='4시간 UD')
    signal = models.CharField(max_length=5, null=True)
    signal_price = models.FloatField(null=True)
    work_two_1_0 = models.CharField(max_length=4, null=True, verbose_name='2개 비교 1.0')
    work_two_1_5 = models.CharField(max_length=4, null=True, verbose_name='2개 비교 1.5')
    work_one_1_0 = models.CharField(max_length=4, null=True, verbose_name='1개 비교 1.0')
    work_one_1_5 = models.CharField(max_length=4, null=True, verbose_name='1개 비교 1.5')
    
    def __str__(self):
        return str(self.datetime)


class MinuteData(models.Model):
    datetime = models.DateTimeField(verbose_name='시간')
    open_price = models.FloatField(verbose_name='시가')
    min_price = models.FloatField(verbose_name='저가')
    max_price = models.FloatField(verbose_name='고가')
    close_price = models.FloatField(verbose_name='종가')
    avg_price = models.FloatField(verbose_name='평균')
    volume = models.BigIntegerField(verbose_name='거래량')
    volume_rate = models.FloatField(verbose_name='거래량 비')
    volume_up_dn = models.CharField(max_length=2, null=True, verbose_name="거래량 UP/DN")
    up_down = models.CharField(max_length=2, verbose_name='UD')
    continue_up_down = models.CharField(max_length=3, verbose_name='연속 UD')
    hour_up_down = models.CharField(max_length=6, verbose_name='4시간 UD')
    signal = models.CharField(max_length=5, null=True)
    signal_price = models.FloatField(null=True)
    work_two_1_0 = models.CharField(max_length=4, null=True, verbose_name='2개 비교 1.0')
    work_two_1_5 = models.CharField(max_length=4, null=True, verbose_name='2개 비교 1.5')
    work_one_1_0 = models.CharField(max_length=4, null=True, verbose_name='1개 비교 1.0')
    work_one_1_5 = models.CharField(max_length=4, null=True, verbose_name='1개 비교 1.5')
    
    def __str__(self):
        return str(self.datetime)
