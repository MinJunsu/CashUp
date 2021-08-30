from django.urls import path
from .views import TradeResultAPIView

urlpatterns = [
    path('test/', TradeResultAPIView.as_view())
]