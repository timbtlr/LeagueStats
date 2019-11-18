from django.db import models


class Champion(models.Model):
    """
    Champion model.  Represents minimal data about a character that can be played within
    League of Legends.
    """
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.title}"
