import ast
import json

from django.db.models import Q
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

def plan_code_already_exists(plan_code):
    return Plans.objects.filter(plan_code=plan_code).exists()

def build_lookups(queryset):
    if 'ddds' in queryset.keys():
        q_ddds = Q(ddds__contains=ast.literal_eval(queryset['ddds'][0]))

        if 'plan_type' in queryset.keys():
            q_plan_type = Q(plan_type=queryset['plan_type'][0])
        else:
            q_plan_type = Q(plan_type__isnull=False)

        if 'operator' in queryset.keys():
            q_operator = Q(operator=queryset['operator'][0])
        else:
            q_operator = Q(operator__isnull=False)

        if 'plan_code' in queryset.keys():
            q_plan_code = Q(plan_code=queryset['plan_code'][0])
        else:
            q_plan_code = Q(plan_code__isnull=False)

        return (q_ddds, q_plan_type, q_operator, q_plan_code)

@csrf_exempt
def create(request):
    if not request.method == 'POST':
        return error_response(400, 'Bad Request.')

    payload = json.loads(request.body)

    invalid_fields = validates_payload(payload)
    if invalid_fields:
        return error_response(400, 'Bad Request.', invalid_fields)

    if plan_code_already_exists(payload['plan_code']):
        invalid_fields = [{'plan_code': 'already exists.'}]
        return error_response(500, 'Internal Server Error.', invalid_fields)

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

    payload = []
    queryset = dict(request.GET)

    lookups = build_lookups(queryset)

    if lookups:
        q_ddds, q_plan_type, q_operator, q_plan_code = lookups
        plans = Plans.objects.filter(
            q_ddds, q_plan_type, q_operator, q_plan_code)
    else:
        plans = Plans.objects.all()

    if plans:
        for plan in plans:
            payload.append(
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
            )

    status_code = 200 if payload else 404

    response = {
        'data': payload,
        'total': len(payload),
        'status_code': status_code
    }
    return JsonResponse(response, status=status_code)
