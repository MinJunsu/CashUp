from django.urls import path
from .views import ProgressbarAPIView, HourAPIView, MinuteAPIView, UpFlowAPIView, DownFlowAPIView, FlagAPIView

urlpatterns = [
    path('progress/', ProgressbarAPIView.as_view()),
    path('hour/', HourAPIView.as_view()),
    path('minute/', MinuteAPIView.as_view()),
    path('upflow/', UpFlowAPIView.as_view()),
    path('downflow/', DownFlowAPIView.as_view()),
    path('flag/', FlagAPIView.as_view())
]