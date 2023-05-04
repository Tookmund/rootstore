import requests
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError

from .models import Certificate, Root_Store
from .utils import deactivate_certs


def apple_table(url):
    return []

def update():
    root_store = Root_Store.objects.get(name="Apple")
    for cert_row in apple_table(root_store.source):
        fingerprint = cert_row[6].replace(" ", "").lower()
        try:
            cert = Certificate(sha256=fingerprint,
                    common_name=cert_row[0]
            )
            cert.save()
        except IntegrityError:
            cert = Certificate.objects.get(sha256=cert_row)
        cert.stores.add(root_store)
        root_store.certificates.add(cert)

