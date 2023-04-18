from django.db import models

# Create your models here.

class Certificate(models.Model):
    sha256 = models.CharField(max_length=64, unique=True)
    pem = models.CharField(max_length=16384)
    common_name = models.CharField(max_length=512)
    stores = models.ManyToManyField("Root_Store", through="Store_Contents")


class Root_Store(models.Model):
    name = models.CharField(max_length=512, unique=True)
    source = models.URLField(max_length=1000)
    certificates = models.ManyToManyField(Certificate, through="Store_Contents")


class Store_Contents(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    root_store = models.ForeignKey(Root_Store, on_delete=models.CASCADE)
    active = models.BooleanField()
    last_trusted = models.DateTimeField()

    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields=["certificate", "root_store"],
                    name="unique_migration_host_combination"
                )
        ]
