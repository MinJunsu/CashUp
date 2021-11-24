from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers.json import DjangoJSONEncoder

from datetime import datetime, timedelta
import json