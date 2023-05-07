import datetime
from django.db.utils import IntegrityError

from .utils import store_update, csv_reader_from_url, deactivate_certs
from .models import Certificate, Root_Store, Store_Contents


def mozilla_update():
    yield from store_update(csv_reader_from_url, "mozilla",
            fingerprint_key="SHA-256 Fingerprint",
            cn_key="Common Name or Certificate Name",
            owner_key="Owner",
            pem_key="PEM Info")


def microsoft_update():
    yield from store_update(csv_reader_from_url, "microsoft",
            fingerprint_key="SHA-256 Fingerprint",
            cn_key="CA Common Name or Certificate Name",
            owner_key="CA Owner",
            active_key="Microsoft Status",
            active_value="Included")

