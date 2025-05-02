from django.contrib import admin
from .models import receivedDevice,receivedData



admin.site.register(receivedData)
admin.site.register(receivedDevice)
