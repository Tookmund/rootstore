from django.shortcuts import render
from django.http import HttpResponse

from .fetch_rootstores import mozilla_update, microsoft_update

# Create your views here.


def updateCerts(request):
    microsoft_update()
    mozilla_update()
    return HttpResponse("Certs Updated!")
