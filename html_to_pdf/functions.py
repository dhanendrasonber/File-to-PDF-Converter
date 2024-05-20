
from file_to_pdf import settings
import os
import pdfkit
from django.http import HttpResponse

"""Internal Import"""
from django.shortcuts import render

class HtmlToPdf():
    def get_preview(template, page_size):
        """function to convert html to pdf"""
        options = {
            'page-size': page_size,
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
        }
            
        wKHTMLtoPDF_path = settings.WKHTMLTOPDF
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wKHTMLtoPDF_path)
        try:
            pdfkit.from_string(template, 'html_to_pdf/newpdf.pdf', options=options, configuration=pdfkit_config)
        except Exception as e:
            error = f"PDF Generation Error: {e}"
            print(error)
            return error

        pdf = open("html_to_pdf/newpdf.pdf", 'rb')
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        pdf.close()
        os.remove("html_to_pdf/newpdf.pdf")
        return response
    
    def download_file(template, page_size):
        """function to convert html to pdf"""
        options = {
            'page-size': page_size,
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
        }
            
        wKHTMLtoPDF_path = settings.WKHTMLTOPDF
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wKHTMLtoPDF_path)
        try:
            pdfkit.from_string(template, 'html_to_pdf/newpdf.pdf', options=options, configuration=pdfkit_config)
        except Exception as e:
            error = f"PDF Generation Error: {e}"
            print(error)
            return error

        pdf = open("html_to_pdf/newpdf.pdf", 'rb')
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=newpdf.pdf'
        pdf.close()
        os.remove("html_to_pdf/newpdf.pdf")
        return response
    