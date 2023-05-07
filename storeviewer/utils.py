import csv
import io
import requests
import datetime

from django.db.utils import IntegrityError
from .models import Certificate, Root_Store, Store_Contents

def csv_reader_from_url(url):
    response = requests.get(url)
    csv_file = io.StringIO(response.text)
    csv_reader = csv.DictReader(csv_file)
    return csv_reader

def deactivate_certs(root_store, known_certs, current_datetime):
    contents_to_deactivate = Store_Contents.objects.filter(root_store=root_store, active=True).exclude(certificate__in=known_certs)
    for store_contents in contents_to_deactivate:
        store_contents.active = False
        store_contents.last_trusted = current_datetime


def store_update(store_to_iterable_func, store_name, fingerprint_key,
        cn_key=None, owner_key=None, pem_key=None, active_key=None, active_value=None):
    root_store = Root_Store.objects.get(name=store_name)
    current_datetime = datetime.datetime.now(tz=datetime.timezone.utc)
    known_certs = set()
    for cert_row in store_to_iterable_func(root_store.source):
        fingerprint = cert_row[fingerprint_key].lower()
        try:
            cert = Certificate(sha256=fingerprint)
            if cn_key is not None:
                cert.common_name = cert_row[cn_key]
            if owner_key is not None:
                cert.owner = cert_row[owner_key]
            if pem_key is not None:
                cert.pem = cert_row[pem_key].replace("'", "")
            cert.save()
        except IntegrityError:
            cert = Certificate.objects.get(sha256=fingerprint)
        yield fingerprint +": "+cert.owner+", "+cert.common_name+"\n"
        known_certs.add(cert)
        store_contents, created = Store_Contents.objects.get_or_create(
                certificate=cert,
                root_store=root_store,
                defaults={"active": True})
        if active_key is not None and cert_row[active_key] != active_value:
            store_contents.active = False
        if store_contents.active:
            store_contents.last_trusted = current_datetime
        store_contents.save()
    deactivate_certs(root_store, known_certs, current_datetime)


