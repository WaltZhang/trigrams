from django.db import models
from connectors.models import Connector


class Dataset(models.Model):
    name = models.CharField(primary_key=True, max_length=256)
    display_name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    schema = models.TextField()
    sep = models.CharField(max_length=3, blank=True)
    external = models.BooleanField(default=False)
    encoding = models.CharField(max_length=20, blank=True)
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE, blank=True, null=True)
    query_string = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.display_name


class Table(models.Model):
    columns = models.TextField()
    sample = models.TextField()
    schema = models.TextField()
