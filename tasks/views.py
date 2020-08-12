from django.shortcuts import render, redirect
from rest_framework.views import APIView

from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer
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
from common.helper import format_html_date, format_date_only


class NewTask(APIView):
    def get(self, request, jwt_token):
        try:
            try:
                user_data = authrize_user(jwt_token)
            except(jwt.DecodeError, jwt.ExpiredSignatureError):
                return Response({'Message':'Signature has expired'},status=status.HTTP_403_FORBIDDEN)

            all_projects = Project.objects.filter(consumer_id=user_data['user_id'])
            return render(request,'tasks/new_task.html', {'jwt_token': jwt_token, 'all_projects':all_projects})
        except Exception as error:
            return Response(json.dumps({'Message':traceback.format_exc()}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, jwt_token):
        try:
            data=request.data
            data=data.dict()
            try:
                user_data = authrize_user(jwt_token)
            except(jwt.DecodeError, jwt.ExpiredSignatureError):
                return Response({'Message':'Signature has expired'},status=status.HTTP_403_FORBIDDEN)   
            
            must_keys=['name','project','start_time','end_time']
            if bool(set(must_keys)-set(data.keys())):
                error_log = {
                    "from":request.headers.get("Correlation-Id",default_correlation_id),
                    "error":str(set(must_keys)-set(data.keys()))+" missing",
                    "request_data_keys":data.keys()  
                    }
                return Response({'Message':str(set(must_keys)-set(data.keys()))+" missing"},status=status.HTTP_400_BAD_REQUEST)

            data['consumer_id']  = user_data['user_id']
            

            # saving the date in 5 hrs 30 mins before
            data['start_time']  = format_html_date(data['start_time'])
            data['end_time']  = format_html_date(data['end_time'])

            pro = Project.objects.get(id=data['project'])
            pro_ser = ProjectSerializer(pro)
            data['project'] = pro_ser.data['id']


            serializer=TaskSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()

                return redirect('tasks:all_tasks', jwt_token=jwt_token)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message':traceback.format_exc()}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AllTasks(APIView):
    def get(self, request, jwt_token):
        try:
            try:
                user_data = authrize_user(jwt_token)
            except(jwt.DecodeError, jwt.ExpiredSignatureError):
                return Response({'Message':'Signature has expired'},status=status.HTTP_403_FORBIDDEN)   

            tk = Task.objects.filter(consumer_id=user_data['user_id'])

            return render(request,'tasks/all_tasks.html', {'all_tasks': tk, 'jwt_token': jwt_token})
        except Exception as error:
            return Response(json.dumps({'Message':'Internal Server Error'}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, jwt_token):
        try:
            data=request.data
            data=data.dict()
            try:
                user_data = authrize_user(jwt_token)
            except(jwt.DecodeError, jwt.ExpiredSignatureError):
                return Response({'Message':'Signature has expired'},status=status.HTTP_403_FORBIDDEN)   
            
            tk = Task.objects.filter(consumer_id=user_data['user_id'])

            from_date = data['from_date']
            if from_date:
                from_date = format_date_only(from_date)
                tk=tk.filter(created_at__date__gte=from_date)
            
            to_date = data['to_date']
            if to_date:
                to_date = format_date_only(to_date)
                tk=tk.filter(created_at__date__lte=to_date)
            
            return render(request,'tasks/all_tasks.html', {'all_tasks': tk, 'jwt_token': jwt_token})
        except Exception as error:
            return Response(json.dumps({'Message':traceback.format_exc()}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class NewProject(APIView):
    def get(self, request, jwt_token):
        try:
            try:
                user_data = authrize_user(jwt_token)
            except(jwt.DecodeError, jwt.ExpiredSignatureError):
                return Response({'Message':'Signature has expired'},status=status.HTTP_403_FORBIDDEN)
            return render(request,'tasks/new_project.html', {'jwt_token': jwt_token})
        except Exception as error:
            return Response(json.dumps({'Message':traceback.format_exc()}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, jwt_token):
        try:
            data=request.data
            data=data.dict()
            try:
                user_data = authrize_user(jwt_token)
            except(jwt.DecodeError, jwt.ExpiredSignatureError):
                return Response({'Message':'Signature has expired'},status=status.HTTP_403_FORBIDDEN)   
            
            must_keys=['name']
            if bool(set(must_keys)-set(data.keys())):
                error_log = {
                    "from":request.headers.get("Correlation-Id",default_correlation_id),
                    "error":str(set(must_keys)-set(data.keys()))+" missing",
                    "request_data_keys":data.keys()  
                    }
                return Response({'Message':str(set(must_keys)-set(data.keys()))+" missing"},status=status.HTTP_400_BAD_REQUEST)

            data['consumer_id']  = user_data['user_id']

            serializer=ProjectSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()

                return redirect('tasks:new_task', jwt_token=jwt_token)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message':traceback.format_exc()}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

