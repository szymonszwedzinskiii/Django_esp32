
from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.ping),
    path('api/get_data/',views.get_data),
    path('sensor_data/',views.show_sensor_data),
]
