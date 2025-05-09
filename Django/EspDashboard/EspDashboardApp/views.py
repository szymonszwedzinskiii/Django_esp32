from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from django.db.models import Avg,Min,Max
from django.views.decorators.csrf import csrf_exempt
from matplotlib.pyplot import ylabel
from io import BytesIO
from django.db.models.functions import TruncDate
from django.contrib.auth.models import User
from django.contrib import messages

from .models import receivedData,receivedDevice, Alert, UserApiToken
import matplotlib.pyplot as plt
from datetime import datetime
from django.utils.dateparse import parse_datetime



def ping(request):
    return JsonResponse({"message": "Success"})

def startupPage(request):
    user = request.user
    user = User.objects.get(username=user)
    try:
        devices = receivedDevice.objects.filter(owner=user)
    except receivedDevice.DoesNotExist:
        return render(request, 'startupPage.html', {'data': ''})  # todo create dashboard for empty data

    return render(request, "startupPage.html",{'data':devices})

@csrf_exempt
def addDevice(request):
    if request.method == 'POST':
        token = request.POST.get('Token')
    return render(request,'addDevice.html',{})


# @csrf_exempt
# def get_data(request):
#     print('get_data func is working')
#
#     if request.method == "POST":
#         print('POST')
#         try:
#             data = json.loads(request.body)
#             print(data)
#             device_name = data['device_name']
#             temperature = data['temperature']
#             user= data['user']
#             user = User.objects.get(username=user)
#             if temperature is None or device_name is None:
#                 print('Missing data')
#                 return JsonResponse({"Error": "Missing data"})
#             device, _ = receivedDevice.objects.get_or_create(device_name=device_name,owner=user)
#
#             receivedData.objects.create(
#                 temperature = temperature,
#                 device_name= device,
#
#             )
#             return JsonResponse({'status': 'success'}, status=201)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@login_required
def plot_page(request):
    data = receivedData.objects.all()
    return render(request, 'sensor_data.html',{'data': data})

@login_required
def plot_view(request):
    data = receivedData.objects.all().order_by('timestamp')

    timestamps = [entry.timestamp for entry in data]
    temperatures = [entry.temperature for entry in data]

    fig, ax = plt.subplots()
    ax.plot(timestamps,temperatures,label="Temperature", marker =0)
    ax.set(xlabel='Time',ylabel='Temperature', title='Plot of temperature in time')
    ax.grid(True)
    ax.legend()

    buf = BytesIO()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')

@login_required
def show_sensor_data(request):
    data = receivedData.objects.all()
    return render(request, 'sensor_data.html', {'data':data})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('startupPage')
        else:
            messages.error(request, 'Nieprawidłowe dane logowania')

    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def registration_page(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ' Rejestracja zakończona pomyślnie. Możesz się teraz zalogować')
            return redirect('login')
        else:
            messages.error(request,'Rejestracja sie nie powiodla, sprobuj ponownie')
    else:
        form = UserCreationForm()
    return render(request,'register.html',{'form': form})

def user_dashboard(request):
    user = request.user
    user = User.objects.get(username=user)
    try:
        devices = receivedDevice.objects.filter(owner=user)
    except receivedDevice.DoesNotExist:
        return render(request, 'dashboard.html', {'': ''}) # todo create dashboard for empty data

    data = receivedData.objects.filter(device_name__in=devices)

    if not data.exists():
        return render(request, 'dashboard.html', {'': ''})

    if not user.is_authenticated:
        return redirect('login')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        data = data.annotate(date_only=TruncDate('timestamp'))
        data = data.filter(date_only__range=[start_date,end_date])

    stats = data.aggregate(
        avg_temp = Avg("temperature",default=0),
        max_temp=Max("temperature"),
        min_temp = Min("temperature")

    )
    alerts_triggered = []
    for device in devices:
        alerts = Alert.objects.filter(device=device)
        for alert in alerts:
            if data.filter(device_name=device, temperature__gte=alert.temperature_threshold).exists():
                alerts_triggered.append(f"Alert dla {device.device_name}: {alert.message}")

    context = {
        'data':data,
        "stats":stats,
        "start_date":start_date,
        "end_date":end_date,
        'alerts':alerts_triggered

    }
    return render(request, 'dashboard.html',context)

def device_dashboard(request, device_id):
    device = get_object_or_404(receivedDevice, id=device_id)
    received_data = receivedData.objects.filter(device_name=device)
    return render(request, 'dashboard_test.html', {'device': device,
                                              'received_data':received_data})

def device_plot(request, device_id):
    device =get_object_or_404(receivedDevice,id=device_id)
    data = receivedData.objects.filter(device_name=device)
    timestamps = [entry.timestamp for entry in data]
    temperatures = [entry.temperature for entry in data]

    fig, ax = plt.subplots()
    ax.plot(timestamps, temperatures, label="Temperature", marker=0)
    ax.set(xlabel='Time', ylabel='Temperature', title='Plot of temperature in time')
    ax.grid(True)
    ax.legend()

    buf = BytesIO()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')

@login_required
def show_token(request):
    token, created = UserApiToken.objects.get_or_create(user=request.user)
    return render(request, 'show_token.html', {"token":token.token})

@csrf_exempt
def get_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "invalid method"})
    print("TEST")
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Token"):
        return JsonResponse({"error": "missing or invalid Token"})

    token_value = auth.split(" ")[1]
    try:
        api_token = UserApiToken.objects.get(token=token_value)
        user = api_token.user
    except UserApiToken.DoesNotExist:
        return JsonResponse({"error" : "Invalid Token"}, status=403)

    try:
        data = json.loads(request.body)
        device_name= data["device_name"]
        temperature = float(data["temperature"])
        device, _ = receivedDevice.objects.get_or_create(owner = user, device_name=device_name)

        receivedData.objects.create(device_name=device, temperature=temperature)

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    user = request.user
    user = User.objects.get(username=user)
    try:
        devices = receivedDevice.objects.filter(owner=user)
    except receivedDevice.DoesNotExist:
        return render(request, 'startupPage.html', {'data': ''})  # todo create dashboard for empty data

    return render(request, "startupPage.html",{'data':devices})

