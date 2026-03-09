from django.db import models

class Visitor(models.Model):

    ip_address = models.GenericIPAddressField(unique=True)

    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip_address