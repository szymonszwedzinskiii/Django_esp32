
from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.ping),
    path('api/get_data/',views.get_data),
    path('sensor_data/',views.show_sensor_data),
    path('plot/image/', views.plot_view, name='plot_view'),
    path('plot_page/', views.plot_page, name='plot_view'),
]
