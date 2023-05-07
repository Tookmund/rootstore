import requests
from bs4 import BeautifulSoup
import lxml
import cchardet

from cryptography import x509
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import Encoding

from .utils import store_update


def chrome_pems(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    table = soup.find("table")
    pem = b""
    newline = "\n".encode("utf-8")
    is_cert = False
    for line in table.find_all("tr"):
        if line.text == "-----BEGIN CERTIFICATE-----":
            is_cert = True
        if is_cert:
            pem += line.text.encode("utf-8") + newline
        if line.text == "-----END CERTIFICATE-----":
            is_cert = False
            yield pem
            pem = b""


def cn(subject):
    try:
        cn = subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
        if len(cn) > 0:
            return cn[0].value
        else:
            return subject.get_attributes_for_oid(x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value
    except (ValueError, IndexError):
        return None

def chrome_table(url):
    for pem in chrome_pems(url):
        try:
            cert = x509.load_pem_x509_certificate(pem)
        except ValueError:
            continue
        # fingerprint,issuer,common name,pem
        yield [cert.fingerprint(SHA256()).hex(), cn(cert.issuer), cn(cert.subject), pem.decode("utf-8")]

def google_update():
    yield from store_update(chrome_table, "google",
            fingerprint_key=0,
            owner_key=1,
            cn_key=2,
            pem_key=3)
