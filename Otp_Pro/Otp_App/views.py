from . forms import *
from . models import *
from . serializers import *
from . import services
from django.shortcuts import render
from django.contrib.auth.models import User as authUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.parsers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView #API data
from rest_framework.response import Response #Successful 200 response
from rest_framework import status #send back status 
from rest_framework.decorators import api_view
import json, ast
from datetime import datetime, date, timezone
from django.core.mail import send_mail
from django.conf import settings 
import math, random


def home(request):
    data = User.objects.all()
    context = {
                'data':data,
                }
    return render(request, 'home.html',context)

# OTP Generator function
def generateOTP() :
    digits = "12345abcdefghijklmABCDEFGHIJKLMNOPQRSTUVWXYZnopqrstuvwxyz67890"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_otp_mail(email,userid):
    OTP = generateOTP()
    if Email_verification.objects.filter(email=userid).exists():
        Email_verification.objects.filter(email=userid).delete()
        Email_verification.objects.create(email_id=userid,otp=OTP)
    else:
        Email_verification.objects.create(email_id=userid,otp=OTP)

def resend_otp(request,userid):
    email = User.objects.get(id=userid).email
    send_otp_mail(email,userid)
    return HttpResponseRedirect(reverse('verify_email', args=(userid, )))

def verify_email(request,id):
    form = OTP_Verification(request.POST or None)
    template = 'email_verify.html'
    user_otp_time = Email_verification.objects.get(email=id).updated_at
    current_time = datetime.now(timezone.utc)
    time_diff = (current_time - user_otp_time)
    minutes = divmod(time_diff.total_seconds(), 60)  
    total_minutes = minutes[0]
    context = {
                'form':form,
                'minutes':total_minutes,
                'userid':id,
                }
    if (total_minutes < 30.00):
        if request.method =='POST':
            user_OTP = request.POST.get('otp')
            print(user_OTP)
            if Email_verification.objects.filter(email=id,otp=user_OTP).exists():
                Email_verification.objects.filter(email=id).update(enable=True)
                return redirect('/')
            else:
                form = OTP_Verification(request.POST)
    return render(request, template, context)


def register(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_id = User.objects.get(username=username).id
            send_otp_mail(username,user_id)
            return HttpResponseRedirect(reverse('verify_email', args=(user_id, )))
        else:
            form = SignUpForm(request.POST or None)
    return render(request, 'register.html', {'form': form})

def OTP_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')        
        form = OTP_Login(request.POST)
        qs = Email_verification.objects.filter(email__email=email)
        if Email_verification.objects.filter(email__email=email).exists():
            if (qs.filter(otp=otp).exists()):
                if form.is_valid():
                    return redirect('/') 
            else:
                messages.info(request, 'Enter the Correct OTP!')
                return HttpResponseRedirect("/login-otp/")
        else:
            messages.info(request, 'Enter the Correct Email!')
            return HttpResponseRedirect("/login-otp/") 
    else: 
        form = OTP_Login(request.POST or None)   
    return render(request, "login.html", {"form": form})

class LoginData(APIView):

    # permission_classes = (IsAuthenticated,) 

    def get(self, request, format=None):
    	pass

    def post(self, request, format=None):
    	data=self.request.data
    	username = data.get('username')
    	password = data.get('password')
    	if (User.objects.filter(username=username).exists()):
    		user = authenticate(username=username, password=password)
    		login(request, user)
    		return services.MesgResponse(username,mesg="Login Successfully",status=204) 
    	else:
    		return services.MesgResponse(username,mesg="Username is not Exist",status=400) 

