# Generated by Django 3.2.5 on 2021-11-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_hoursubdata_minutesubdata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DownFlow',
        ),
        migrations.DeleteModel(
            name='UpFlow',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='avg_price',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='continue_up_down',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='hour_up_down',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='signal',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='up_down',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='volume_rate',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='volume_up_dn',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='work_one_1_0',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='work_one_1_5',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='work_two_1_0',
        ),
        migrations.RemoveField(
            model_name='hourdata',
            name='work_two_1_5',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='avg_price',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='continue_up_down',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='hour_up_down',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='signal',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='up_down',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='volume_rate',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='volume_up_dn',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='work_one_1_0',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='work_one_1_5',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='work_two_1_0',
        ),
        migrations.RemoveField(
            model_name='hoursubdata',
            name='work_two_1_5',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='avg_price',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='continue_up_down',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='flow',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='hour_up_down',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='signal',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='up_down',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='volume_rate',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='volume_up_dn',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='work_one_1_0',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='work_one_1_5',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='work_two_1_0',
        ),
        migrations.RemoveField(
            model_name='minutedata',
            name='work_two_1_5',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='avg_price',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='continue_up_down',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='flow',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='hour_up_down',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='signal',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='up_down',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='volume_rate',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='volume_up_dn',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='work_one_1_0',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='work_one_1_5',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='work_two_1_0',
        ),
        migrations.RemoveField(
            model_name='minutesubdata',
            name='work_two_1_5',
        ),
        migrations.AddField(
            model_name='hourdata',
            name='time',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='hoursubdata',
            name='time',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='minutedata',
            name='time',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='minutesubdata',
            name='time',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='hourdata',
            name='close_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hourdata',
            name='datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='hourdata',
            name='max_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hourdata',
            name='min_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hourdata',
            name='open_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hourdata',
            name='volume',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='hoursubdata',
            name='close_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hoursubdata',
            name='datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='hoursubdata',
            name='max_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hoursubdata',
            name='min_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hoursubdata',
            name='open_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hoursubdata',
            name='volume',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='minutedata',
            name='close_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='minutedata',
            name='datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='minutedata',
            name='max_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='minutedata',
            name='min_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='minutedata',
            name='open_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='minutedata',
            name='volume',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='minutesubdata',
            name='close_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='minutesubdata',
            name='datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='minutesubdata',
            name='max_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='minutesubdata',
            name='min_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='minutesubdata',
            name='open_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='minutesubdata',
            name='volume',
            field=models.IntegerField(),
        ),
    ]
