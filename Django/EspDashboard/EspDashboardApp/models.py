import secrets

from django.db import models
from django.contrib.auth.models import User

class receivedDevice(models.Model):
    device_name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    token = models.CharField(max_length=64, unique=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(32)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.device_name

class receivedData(models.Model):
    device_name = models.ForeignKey(receivedDevice, on_delete=models.CASCADE)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Alert(models.Model):
    device = models.ForeignKey(receivedDevice, on_delete=models.CASCADE, related_name='alerts')
    temperature_threshold = models.FloatField()
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)