import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Plans
from . import lists


def error_response(status_code, exception, invalid_fields=None):
    response_error = {
        'error': {
            'code': status_code,
            'message': exception
        }
    }

    if invalid_fields:
        response_error['error']['invalid_fields'] = invalid_fields

    return JsonResponse(response_error, status=status_code)

def validates_payload(payload):
    invalid_fields = []

    for key in payload:
        if not payload[key]:
            invalid_fields.append({key: 'is empty'})

    try:
        int(payload['minutes'])
    except ValueError:
        invalid_fields.append({'minutes': 'is not a valid number.'})

    try:
        float(payload['price'])
    except ValueError:
        invalid_fields.append({'price': 'is not a valid number.'})

    if payload['plan_type'] not in lists.PLAN_TYPES_CHOICE:
        invalid_fields.append({'plan_type': 'is not a valid choice.'})

    for ddd in payload['ddds']:
        if ddd not in lists.DDDS_CHOICE:
            invalid_fields.append({'ddds': 'is not a valid choice.'})

    return invalid_fields

@csrf_exempt
def create(request):
    if not request.method == 'POST':
        return error_response(400, 'Bad Request.')

    payload = json.loads(request.body)

    invalid_fields = validates_payload(payload)
    if invalid_fields:
        return error_response(400, 'Bad Request.', invalid_fields)

    try:
        plan = Plans(
            plan_code=payload['plan_code'],
            minutes=int(payload['minutes']),
            internet=payload['internet'],
            price=float(payload['price']),
            plan_type=payload['plan_type'],
            operator=payload['operator'],
            ddds=payload['ddds']
        )
        plan.save()
    except Exception:
        error_response(500, 'Internal Server Error')

    response = {
        'data': [
            {
                'id': plan.id,
                'plan_code': plan.plan_code,
                'minutes': plan.minutes,
                'internet': plan.internet,
                'price': plan.price,
                'plan_type': plan.plan_type,
                'operator': plan.operator,
                'ddds': plan.ddds
            }
        ],
        'status_code': 200
    }
    return JsonResponse(response, status=200)

@csrf_exempt
def update(request, plan_id):
    if request.method not in ['POST', 'PUT']:
        return error_response(400, 'Bad Request.')

    payload = json.loads(request.body)

    response = {
        'data': [
            {
                'id': plan_id,
                'plan_code': 'timpre200',
                'minutes': 200,
                'internet': '20GB',
                'price': 99.90,
                'plan_type': 'Pré',
                'operator': 'Tim',
                'ddds': [21,22]
            }
        ]
    }
    return JsonResponse(response)

@csrf_exempt
def delete(request, plan_id):
    if not request.method == 'POST':
        return error_response(400, 'Bad Request.')

    payload = json.loads(request.body)

    response = {
        'data': [
            {
                'id': plan_id,
                'plan_code': 'timpre200',
                'minutes': 200,
                'internet': '20GB',
                'price': 99.90,
                'plan_type': 'Pré',
                'operator': 'Tim',
                'ddds': [21,22]
            }
        ]
    }
    return JsonResponse(response)

@csrf_exempt
def list(request):
    if not request.method == 'GET':
        return error_response(400, 'Bad Request.')

    response = {
        'data': [
            {
                'id': 1,
                'plan_code': 'timpre200',
                'minutes': 200,
                'internet': '20GB',
                'price': 99.90,
                'plan_type': 'Pré',
                'operator': 'Tim',
                'ddds': [21,22]
            },
            {
                'id': 2,
                'plan_code': 'oipos150',
                'minutes': 150,
                'internet': '15GB',
                'price': 49.90,
                'plan_type': 'Pós',
                'operator': 'Oi',
                'ddds': [11]
            },
        ]
    }
    return JsonResponse(response, safe=False, status=200)
