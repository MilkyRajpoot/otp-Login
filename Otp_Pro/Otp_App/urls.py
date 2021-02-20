from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
# Register and Login/Logout
    path('register/', views.register, name='register'),
    url(r'^otp_verify/(?P<id>\d+)/$', views.verify_email, name='verify_email'),
    url(r'^resend_otp/(?P<userid>\d+)/$', views.resend_otp, name='resend_otp'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="login.html"), name='logout'),
    path('loginApi/', views.LoginData.as_view(),name='LoginData'),
    path('login-otp/', views.OTP_login, name='OTP_login'),

    ]