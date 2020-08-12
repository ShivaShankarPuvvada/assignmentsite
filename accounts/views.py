from django.shortcuts import render, redirect, reverse
from rest_framework.views import APIView

from .models import Consumer
from .serializers import ConsumerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
import jwt
from django.http import JsonResponse
from .auth import authrize_user
import logging
import json
import traceback
from django.conf import settings
from django.db.models import Q


# Create your views here.
class ConsumerCreate(APIView):
    def get(self, request):
        return render(request, 'accounts/signup.html')
    def post(self,request):
        try:
            data=request.data
            data = data.dict()
            must_keys=['password','mobile_number','user_name','email']
            for each in must_keys:
                if each not in data.keys():
                    raise Exception('required key {} is missing'.format(each))
            data['password']=make_password(data['password'])
            serializer=ConsumerSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                return render(request, 'accounts/login.html')
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message':'Internal Server Error'}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConsumerLogin(APIView):
    def get(self, request):
        return render(request, 'accounts/login.html')
    def post(self, request):
        try:
            data = request.data
            data = data.dict()
            name=data['name']
            try:
                js=Consumer.objects.get(Q(email=name) | Q(user_name=name) | Q(mobile_number=name))
            except Consumer.DoesNotExist:
                js=None
            if(js):
                logedIn=check_password(request.data['password'],js.password)
                if(logedIn):
                        from datetime import datetime,timedelta
                        payload = {
                            'user_name':js.user_name,
                            'email':js.email,
                            'user_id':js.id,
                            'is_consumer': True,
                            'exp': datetime.utcnow() + timedelta(seconds=1000)
                        }
                        encoded = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
                        payload = jwt.decode(encoded.decode('utf-8'), settings.JWT_SECRET, algorithm=['HS256'])
                        
                        return redirect('tasks:new_task', jwt_token='Bearer {}'.format(encoded.decode('utf-8')))
                else:
                    return Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            return Response(json.dumps({'Message': traceback.format_exc()}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def logout(request):
    return render(request, 'accounts/logout.html')