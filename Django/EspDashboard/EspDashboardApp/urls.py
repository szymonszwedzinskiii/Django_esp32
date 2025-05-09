
from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.ping),
    path('api/get_data/',views.get_data),
    path('sensor_data/',views.show_sensor_data),
    path('plot/image/', views.plot_view, name='plot_view'),
    path('plot_page/', views.plot_page, name='plot_page'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.registration_page,name='register'),
    path('dashboard/',views.user_dashboard,name='dashboard'),
    path('dashboard/<int:device_id>/',views.device_dashboard,name='device_dashboard'),
    path('plot/<int:device_id>/',views.device_plot,name='device_plot'),
    path('startupPage/',views.startupPage,name='startupPage'),
    path('add_device/', views.addDevice, name='addDevice'),
    path('show_token/', views.show_token, name='showToken'),
]
