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
from .functions import HtmlToPdf
from .serializers import HTMLSerializer
from helper.functions import *

class CovertHtmltoPDF(generics.CreateAPIView):
    """
    API to convert Html template into PDF
    
    HEAD PARAM: None
    PATH PARAMS: None
    QUERYSTRING PARAMS: "page_size"
    API RESPONSE: PDF Preview
    """
    serializer_class = HTMLSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data = data)
        if not serializer.is_valid():
            errors = serializer.errors
            err = error_message_function(errors)
            return Response(ResponseHandling.success_response_message(err, {}), status=status406)
        html = serializer.validated_data['html_file']
        page_size = serializer.validated_data['page_size']
        
        request_type = kwargs.get('param')
        if html.content_type == 'text/html':
            
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
                html_file = html.read().decode('utf-8')
                pdf = pdfkit.from_string(html_file, False, options=options, configuration=pdfkit_config)
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
            return Response({'detail': 'Uploaded file is not HTML content.', 'result':{}}, status=status400)
        

              