from django.db import models


class Champion(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
