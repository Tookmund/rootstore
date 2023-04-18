from django.urls import path

from .views import updateCerts

urlpatterns = [
    path("update", updateCerts, name="update"),
]
