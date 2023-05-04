import csv
import io
import requests

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


