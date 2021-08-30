from rest_framework.serializers import ModelSerializer
from .models import TradeResult

class TradeResultModelSerializer(ModelSerializer):
    class Meta:
        model = TradeResult
        fields = '__all__'