from django.db import models

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    last_seen = models.DateTimeField(auto_now=True)