from django.urls import path

from .views import homePage, updateCerts, viewStore, viewCert

urlpatterns = [
    path("", homePage),
    path("update", updateCerts, name="update"),
    path("rootstore/<name>", viewStore),
    path("cert/<sha256>", viewCert),
]
