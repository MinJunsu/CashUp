from rest_framework.serializers import ModelSerializer
from .models import HourData, MinuteData, UpFlow, DownFlow

class HourDataModelSerializer(ModelSerializer):
    class Meta:
        model = HourData
        fields = '__all__'

class MinuteDataModelSerializer(ModelSerializer):
    class Meta:
        model = MinuteData
        fields = '__all__'

class UpFlowModelSerializer(ModelSerializer):
    class Meta:
        model = UpFlow
        fields = '__all__'

class DownFlowModelSerializer(ModelSerializer):
    class Meta:
        model = DownFlow
        fields = '__all__'