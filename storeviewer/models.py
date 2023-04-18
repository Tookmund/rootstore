from django.db import models

# Create your models here.

class Certificate(models.Model):
    sha256 = models.CharField(max_length=64, unique=True)
    pem = models.CharField(max_length=16384)
    common_name = models.CharField(max_length=512)
    stores = models.ManyToManyField("Root_Store")


class Root_Store(models.Model):
    name = models.CharField(max_length=512, unique=True)
    source = models.URLField(max_length=1000)
    certificates = models.ManyToManyField(Certificate)

