from django.db import models
class EmailValid(models.Model):
    value = models.CharField(max_length = 32)
    email_address = models.EmailField()
    times = models.DateTimeField()

class user(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=64)