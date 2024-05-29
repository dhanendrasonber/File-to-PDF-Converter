from rest_framework import status

class ResponseHandling:
    def failure_response_message(detail,result):
        """
        error message for failure
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'detail' : detail, 'result' : result}

    def success_response_message(detail,result):
        """
        success message for Success
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'detail' : detail, 'result' : result}
    


status200 = status.HTTP_200_OK
status201 = status.HTTP_201_CREATED
status202 = status.HTTP_202_ACCEPTED
status204 = status.HTTP_204_NO_CONTENT
status400 = status.HTTP_400_BAD_REQUEST
status401 = status.HTTP_401_UNAUTHORIZED
status403 = status.HTTP_403_FORBIDDEN
status404 = status.HTTP_404_NOT_FOUND
status406 = status.HTTP_406_NOT_ACCEPTABLE


#-------------------------------------- ERROR GENERAL FUNCTIONS ------------------------------------

def error_message_function(errors):
    """
    return error message when serializer is not valid
    :param errors: error object
    :returns: string
    """
    for key, values in errors.items():
        if isinstance(values, list):
            error = [value[:] for value in values]
        else:
            error = [str(values)]  # Handle non-list values
        err = ' '.join(map(str, error))
        return err
    



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
    