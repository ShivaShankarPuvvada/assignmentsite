from django.shortcuts import render
from rest_framework.views import APIView
from accounts.models import Employe
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
import jwt
from .auth import authrize_user
import json
import traceback
import xlsxwriter
from io import StringIO as s_tio

import pandas as pd

from datetime import date
today = date.today()
d1 = today.strftime("%d/%m/%Y")


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


def inde(request):
    if request.method == 'POST':
        e = Employe.objects.all()
        names = []
        ages = []
        dates = []
        for i in e:
            names.append(i.name)
            ages.append(i.age)
            dates.append(d1)

        df1 = pd.DataFrame({"Name": names, "Date": dates})
        df2 = pd.DataFrame({"Age": ages, "Date": dates})
        
        writer = pd.ExcelWriter('name_age.xlsx', engine='xlsxwriter')

        df1.to_excel(writer, index=False, sheet_name="Names")
        df2.to_excel(writer, index=False, sheet_name="Ages")

        writer.save()
        excel = open("name_age.xlsx", "rb")
        # output = s_tio(excel.read())
        # out_content = output.getvalue()
        # output.close()


        response = HttpResponse(excel,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=name_age.xlsx'

        return response

    return render(request, 'inde.html')