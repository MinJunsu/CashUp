from django import urls
from django.urls import path
from .views import ProgressbarAPIView

urlpatterns = [
    path('progress/', ProgressbarAPIView.as_view()),
]