import datetime
from django.db.utils import IntegrityError

from .utils import csv_reader_from_url
from .models import Certificate, Root_Store, Store_Contents

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

        store_contents = Store_Contents(certificate=cert,
                root_store=root_store,
                active=cert_csv["Microsoft Status"] != "Included",
                last_trusted=current_datetime)
        store_contents.save()
