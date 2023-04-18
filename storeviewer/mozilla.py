from django.db.utils import IntegrityError

from .utils import csv_reader_from_url
from .models import Certificate, Root_Store

def update():
    root_store = Root_Store.objects.get(name="Mozilla")
    for cert_csv in csv_reader_from_url(root_store.source):
        try:
            cert = Certificate(sha256=cert_csv["SHA-256 Fingerprint"].upper(),
                    common_name=cert_csv["Common Name or Certificate Name"],
                    pem=cert_csv["PEM Info"],
            )
            cert.save()
        except IntegrityError:
            cert = Certificate.objects.get(sha256=cert_csv["SHA-256 Fingerprint"])
        cert.stores.add(root_store)
        root_store.certificates.add(cert)

