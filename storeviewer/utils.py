import csv
import io
import requests

def csv_reader_from_url(url):
    response = requests.get(url)
    csv_file = io.StringIO(response.text)
    csv_reader = csv.DictReader(csv_file)
    return csv_reader

