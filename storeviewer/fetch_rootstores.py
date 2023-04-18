import datetime
from django.db.utils import IntegrityError

from .utils import csv_reader_from_url
from .models import Certificate, Root_Store, Store_Contents

def mozilla_update():
    root_store = Root_Store.objects.get(name="Mozilla")
    current_datetime = datetime.datetime.now(tz=datetime.timezone.utc)
    for cert_csv in csv_reader_from_url(root_store.source):
        try:
            cert = Certificate(sha256=cert_csv["SHA-256 Fingerprint"].upper(),
                    common_name=cert_csv["Common Name or Certificate Name"],
                    pem=cert_csv["PEM Info"],
            )
            cert.save()
        except IntegrityError:
            cert = Certificate.objects.get(sha256=cert_csv["SHA-256 Fingerprint"])



def microsoft_update():
    root_store = Root_Store.objects.get(name="Microsoft")
    current_datetime = datetime.datetime.now(tz=datetime.timezone.utc)
    for cert_csv in csv_reader_from_url(root_store.source):
        try:
            cert = Certificate(sha256=cert_csv["SHA-256 Fingerprint"].upper(),
                    common_name=cert_csv["CA Common Name or Certificate Name"],
            )
            cert.save()
        except IntegrityError:
            cert = Certificate.objects.get(sha256=cert_csv["SHA-256 Fingerprint"])

        store_contents, created = Store_Contents.objects.get_or_create(
                certificate=cert,
                root_store=root_store)

        store_contents.active = cert_csv["Microsoft Status"] != "Included"
        store_contents.last_trusted=current_datetime
        store_contents.save()
