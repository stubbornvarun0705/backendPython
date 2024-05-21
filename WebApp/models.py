from django.db import models

class GoogleAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
