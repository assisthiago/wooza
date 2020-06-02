import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create(request):
    if not request.POST:
        pass

    response = {
        'data': [
            {
                'id': 1,
                'plan_code': 'Tim Pré 200',
                'minutes': 200,
                'internet': 20,
                'price': 99.90,
                'plan_type': 'Pré',
                'operator': 'Tim',
                'ddd': [21,22]
            }
        ]
    }
    return JsonResponse(response)

@csrf_exempt
def update(request, plan_id):
    if not request.POST or not request.PUT:
        pass

    response = {
        'data': [
            {
                'id': plan_id,
                'plan_code': 'Tim Pré 200',
                'minutes': 200,
                'internet': 20,
                'price': 99.90,
                'plan_type': 'Pré',
                'operator': 'Tim',
                'ddd': [21,22]
            }
        ]
    }
    return JsonResponse(response)

@csrf_exempt
def delete(request, plan_id):
    if not request.POST:
        pass

    response = {
        'data': [
            {
                'id': plan_id,
                'plan_code': 'Tim Pré 200',
                'minutes': 200,
                'internet': 20,
                'price': 99.90,
                'plan_type': 'Pré',
                'operator': 'Tim',
                'ddd': [21,22]
            }
        ]
    }
    return JsonResponse(response)

@csrf_exempt
def list(request):
    if not request.GET:
        pass

    response = {
        'data': [
            {
                'id': 1,
                'plan_code': 'Tim Pré 200',
                'minutes': 200,
                'internet': 20,
                'price': 99.90,
                'plan_type': 'Pré',
                'operator': 'Tim',
                'ddd': [21,22]
            },
            {
                'id': 2,
                'plan_code': 'Oi Pós 150',
                'minutes': 150,
                'internet': 15,
                'price': 49.90,
                'plan_type': 'Pós',
                'operator': 'Oi',
                'ddd': [11]
            },
        ]
    }
    return JsonResponse(response, safe=False, status=200)
