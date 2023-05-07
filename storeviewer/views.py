from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse

from .ccadb_rootstores import mozilla_update, microsoft_update
from .apple import apple_update
from .google import google_update

from .models import Root_Store, Certificate, Store_Contents

# Create your views here.


def updateCerts(request):
    return StreamingHttpResponse(streamUpdateCerts())

def streamUpdateCerts():
    yield "<pre>"
    yield "Begin Certs Update...\n"
    yield "Mozilla...\n"
    yield from mozilla_update()
    yield "Microsoft...\n"
    yield from microsoft_update()
    yield "Apple...\n"
    yield from apple_update()
    yield "Google...\n"
    yield from google_update()
    yield "All Updates Complete!\n"
    yield "</pre>"


def homePage(request):
    return render(request, "storeviewer/homepage.html",
            context={
                "rootstores": Root_Store.objects.all()
                })



def viewStore(request, name):
    root_store = Root_Store.objects.get(name=name)

    return render(request, "storeviewer/rootstore.html",
            context={"rootstore": root_store,
                "store_contents": Store_Contents.objects.filter(root_store=root_store)
                })


def viewCert(request, sha256):
    cert = Certificate.objects.get(sha256=sha256)
    return render(request, "storeviewer/certificate.html",

            context={
                "certificate": cert,
                "stores": cert.stores.all()
                })
