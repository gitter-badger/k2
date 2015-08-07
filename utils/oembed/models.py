from django.db import models

thumbnail_url = models.CharField(max_length=255, blank=True, null=True)

def db_type(**kwargs):
    return None

match = models.CharField(max_length=255)

