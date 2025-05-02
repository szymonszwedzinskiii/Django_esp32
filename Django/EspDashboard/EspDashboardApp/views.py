from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import receivedData,receivedDevice

def ping(request):
    return JsonResponse({"message": "Success"})

@csrf_exempt
def get_data(request):
    print('get_data func is working')

    if request.method == "POST":
        print('POST')
        try:
            data = json.loads(request.body)
            device_name = data.get('device_name')
            temperature = data.get('temperature')
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

def show_sensor_data(request):
    data = receivedData.objects.all()
    return render(request, 'sensor_data.html', {'data':data})