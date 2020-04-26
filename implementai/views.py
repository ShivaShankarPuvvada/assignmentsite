from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


from django.shortcuts import render

from .models import Student, StudentDetails
from .serializers import StudentSerializer, StudentDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
import jwt
from django.http import JsonResponse, QueryDict
from .auth import authrize_user
import logging
import json
import re
import traceback


class StudentCreate(APIView):
    def post(self,request):
        try:
            data=request.data
            # data = QueryDict.itervalues(data)
            data = dict(data)
            data['country_code'] = ['+91']

            # must_keys=['password','country_code','mobile_number','user_name','email']
            # for each in must_keys:
            #     if each not in data.keys():
            #         raise Exception('required key {} is missing'.format(each))
            
            data['password']=make_password(data['password'])
            serializer=StudentSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            import pdb; pdb.set_trace()
            return Response(json.dumps({'Message':'Internal Server Error'}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):
        return render(request, 'signup.html')


class StudentLogin(APIView):
    def post(self, request):
        try:
            email=request.data['email']
            try:
                js=Student.objects.get(email=email)
            except Student.DoesNotExist:
                js=None
            if(js):
                logedIn=check_password(request.data['password'],js.password)
                if(logedIn):
                    import json
                    from datetime import datetime,timedelta
                    payload =   {
                                    'user_name':js.user_name,
                                    'email':js.email,
                                    'user_id':js.id,
                                    'is_jobseeker':True,
                                    'exp': datetime.utcnow() + timedelta(seconds=1000000)
                                }
                    encoded = jwt.encode(payload, 'secret', algorithm='HS256')
                    return JsonResponse({'jwt':encoded.decode('utf-8')})
                else:
                    return Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):
        return render(request, 'login.html')

