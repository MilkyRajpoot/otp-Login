from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User

class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'     

# class dealSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Deals
#         fields = '__all__'   