# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext


from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from searcher import SearchClass
from django.http import HttpResponse
from django.conf import settings


#@api_view(['GET', 'POST'])

def home(request, template_name="indexer.html"):
    """
    A index view.
    """
    return render_to_response(template_name,
                              context_instance=RequestContext(request))


class SearchRest(APIView):
    def get(self, request, job, *args, **kw):
        search_data = str(job)

        if search_data:
            myClass = SearchClass()
            result = myClass.scrape_jobs(search_data, *args, **kw)
            response = Response(result, status=status.HTTP_200_OK, content_type='json')
        else:
           response = Response(status = status.HTTP_404_NOT_FOUND)

        return response

class SearchStay(APIView):
    def get(self, request, job, site, *args, **kw):
        search_data = str(job)
        site = str(site)

        if search_data:
            myClass = SearchClass()
            result = myClass.scrape_sites(site, search_data, 50, 68106 *args, **kw)
            response = Response(result, status=status.HTTP_200_OK, content_type='json')
        else:
           response = Response(status = status.HTTP_404_NOT_FOUND)

        return response

# Receives Email from MailGun
#http://www.mettentot.com/years/api/messages/
class EmailIn(APIView):
    def post(self, request):
         if request.method == 'POST':

             sender    = request.POST.get('sender')
             recipient = request.POST.get('recipient')
             subject   = request.POST.get('subject', '')

             body_plain = request.POST.get('body-plain', '')
             body_without_quotes = request.POST.get('stripped-text', '')

             #writing to a file for debugging purposes
             path1 = settings.MEDIA_ROOT
             filename = path1 + '/11data.txt'
             file = open(filename, 'w+')
             file.write(sender + recipient + subject + body_plain + body_without_quotes)
             # note: other MIME headers are also posted here...

             # attachments:
             for key in request.FILES:
                 file = request.FILES[key]
                 # do something with the file

         # Returned text is ignored but HTTP status code matters:
         # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
         return HttpResponse('OK')