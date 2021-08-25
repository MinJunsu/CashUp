from django import urls
from django.urls import path
from .views import ProgressbarAPIView, DataAPIView

urlpatterns = [
    path('progress/', ProgressbarAPIView.as_view()),
    path('data/', DataAPIView.as_view()),
]