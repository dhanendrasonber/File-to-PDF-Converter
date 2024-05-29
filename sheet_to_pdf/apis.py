"""External Imports"""
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import AllowAny
from file_to_pdf import settings
import os
import pdfkit
from django.http import HttpResponse
from django.template import loader

"""Internal Imports"""
from helper.functions import *
from .serializers import ExcelSerializer
from helper.functions import *
import pandas as pd

class CovertExceltoPDF(generics.CreateAPIView):
    """
    API to convert Html template into PDF
    
    HEAD PARAM: None
    PATH PARAMS: None
    QUERYSTRING PARAMS: "page_size"
    API RESPONSE: PDF Preview
    """
    serializer_class = ExcelSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data = data)
        if not serializer.is_valid():
            errors = serializer.errors
            err = error_message_function(errors)
            print("yes that the issue")
            return Response(ResponseHandling.success_response_message(err, {}), status=status406)
        excel = serializer.validated_data['excel_file']
        page_size = serializer.validated_data['page_size']
        
        request_type = kwargs.get('param')
        if excel.content_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:

            df = pd.read_excel(excel)
            html = df.to_html()
            print(html)
            
            options = {
                'page-size': page_size,
                'margin-top': '0.2in',
                'margin-right': '0.2in',
                'margin-bottom': '0.2in',
                'margin-left': '0.2in',
                "enable-local-file-access": ""
                
            } 
            wKHTMLtoPDF_path = settings.WKHTMLTOPDF
            pdfkit_config = pdfkit.configuration(wkhtmltopdf=wKHTMLtoPDF_path)
            try:
                # html_file = html.read().decode('utf-8')
                pdf = pdfkit.from_string(html, False, options=options, configuration=pdfkit_config)
            except Exception as e:
                response = f"PDF Generation Error: {e}"
                return Response(response)
            response = HttpResponse(pdf, content_type='application/pdf')
            if request_type == "preview":
                return response
            elif request_type == "download":
                response['Content-Disposition'] = f'attachment; filename=new_pdf.pdf'
                return response
            else:
                return Response({'detail': 'Provide Appropriate request_type', 'result':{}}, status=status400)
        else:
            return Response({'detail': 'Uploaded file is not Excel content.', 'result':{}}, status=status400)
        

              