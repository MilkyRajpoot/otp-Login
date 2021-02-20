from django.http import JsonResponse, HttpResponse
from .models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
import json
from rest_framework import status 

# Method to print Messgae
def MesgResponse(objects,mesg,status):
    return JsonResponse({
        "results":mesg,
        "status":status
        },safe=False)
