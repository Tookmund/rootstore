import requests
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError

from .models import Certificate, Root_Store
from .utils import store_update, deactivate_certs


def apple_table(url):
    stores_response = requests.get(url)
    soup = BeautifulSoup(stores_response.content)

    current_header = soup.find(string="Current Trust Store")
    current_link = current_header.find_next("a")
    current_url = current_link["href"]

    current_store_response = requests.get(current_url)
    current_soup = BeautifulSoup(current_store_response.content)
    current_table = current_soup.find("table")
    current_rows = current_table.find_all("tr")

    root_store_rows = []
    for row in current_rows:
        data = []
        for td in row.find_all("td"):
            data.append(td.text.replace("\xa0", ""))
        if len(data) == 9:
            data[8] = data[8].replace(" ", "").lower()
            root_store_rows.append(data)

    del root_store_rows[0]
    return root_store_rows


def apple_update():
    store_update(apple_table, "apple",
            fingerprint_key=8,
            cn_key=0,
            owner_key=1)
