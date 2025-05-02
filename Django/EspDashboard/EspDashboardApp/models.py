from django.db import models

class receivedDevice(models.Model):
    device_name = models.CharField(max_length=20)

    def __str__(self):
        return self.device_name

class receivedData(models.Model):
    device_name = models.ForeignKey(receivedDevice, on_delete=models.CASCADE)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
