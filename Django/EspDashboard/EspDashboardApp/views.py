from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from matplotlib.pyplot import ylabel
from io import BytesIO

from .models import receivedData,receivedDevice
import matplotlib.pyplot as plt



def ping(request):
    return JsonResponse({"message": "Success"})

@csrf_exempt
def get_data(request):
    print('get_data func is working')

    if request.method == "POST":
        print('POST')
        try:
            data = json.loads(request.body)
            device_name = data['device_name']
            temperature = data['temperature']
            if temperature is None or device_name is None:
                print('Missing data')
                return JsonResponse({"Error": "Missing data"})
            device, _ = receivedDevice.objects.get_or_create(device_name=device_name)

            receivedData.objects.create(
                temperature = temperature,
                device_name= device,
            )
            return JsonResponse({'status': 'success'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

def plot_page(request):
    data = receivedData.objects.all()
    return render(request, 'sensor_data.html',{'data': data})

def plot_view(request):
    data = receivedData.objects.all().order_by('timestamp')

    timestamps = [entry.timestamp for entry in data]
    temperatures = [entry.temperature for entry in data]

    fig, ax = plt.subplots()
    ax.plot(timestamps,temperatures,label="Tempratura", marker =0)
    ax.set(xlabel='Czas',ylabel='Temperatura', title='Wykres temperatury w czasie')
    ax.grid(True)
    ax.legend()

    buf = BytesIO()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')

def show_sensor_data(request):
    data = receivedData.objects.all()
    return render(request, 'sensor_data.html', {'data':data})