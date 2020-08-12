from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
import jwt
from .auth import authrize_user
import json
import traceback


class Docs(APIView):
    def get(self, request, jwt_token):
        try:
            try:
                user_data = authrize_user(jwt_token)
            except(jwt.DecodeError, jwt.ExpiredSignatureError):
                return Response({'Message':'Signature has expired'},status=status.HTTP_403_FORBIDDEN)
            return render(request,'docs.html', {'jwt_token': jwt_token})
        except Exception as error:
            return Response(json.dumps({'Message':traceback.format_exc()}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
