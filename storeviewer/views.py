from django.shortcuts import render
from django.http import HttpResponse

from .ccadb_rootstores import mozilla_update, microsoft_update

from .models import Root_Store, Certificate, Store_Contents

# Create your views here.


def updateCerts(request):
    microsoft_update()
    mozilla_update()
    return HttpResponse("Certs Updated!")


def homePage(request):
    return render(request, "storeviewer/homepage.html",
            context={
                "rootstores": Root_Store.objects.all()
                })



def viewStore(request, name):
    root_store = Root_Store.objects.get(name=name)

    return render(request, "storeviewer/rootstore.html",
            context={"rootstore": root_store,
                "certificates": root_store.certificates.all()
                })


def viewCert(request, sha256):
    cert = Certificate.objects.get(sha256=sha256)
    return render(request, "storeviewer/certificate.html",

            context={
                "certificate": cert,
                "stores": cert.stores.all()
                })
