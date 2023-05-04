import datetime
from django.db.utils import IntegrityError

from .utils import csv_reader_from_url, deactivate_certs
from .models import Certificate, Root_Store, Store_Contents


def ccadb_update(store_name, fingerprint_key, cn_key=None, pem_key=None, active_key=None, active_value=None):
    root_store = Root_Store.objects.get(name=store_name)
    current_datetime = datetime.datetime.now(tz=datetime.timezone.utc)
    known_certs = set()
    for cert_csv in csv_reader_from_url(root_store.source):
        fingerprint = cert_csv[fingerprint_key].lower()
        try:
            cert = Certificate(sha256=fingerprint)
            if cn_key is not None:
                cert.common_name = cert_csv[cn_key]
            if pem_key is not None:
                cert.pem = cert_csv[pem_key]
            cert.save()
        except IntegrityError:
            cert = Certificate.objects.get(sha256=fingerprint)
        known_certs.add(cert)
        store_contents, created = Store_Contents.objects.get_or_create(
                certificate=cert,
                root_store=root_store,
                defaults={"active": True})
        if active_key is not None and cert_csv[active_key] != active_value:
            store_contents.active = False
        if store_contents.active:
            store_contents.last_trusted = current_datetime
        store_contents.save()
    deactivate_certs(root_store, known_certs, current_datetime)


def mozilla_update():
    ccadb_update("mozilla",
            fingerprint_key="SHA-256 Fingerprint",
            cn_key="Common Name or Certificate Name",
            pem_key="PEM Info")


def microsoft_update():
    ccadb_update("microsoft",
            fingerprint_key="SHA-256 Fingerprint",
            cn_key="CA Common Name or Certificate Name",
            active_key="Microsoft Status",
            active_value="Included")

