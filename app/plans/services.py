import ast
import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Plans
from . import lists
from . import helpers


@csrf_exempt
def create(request):
    if not request.method == 'POST':
        return helpers.error_response(400, 'Bad Request.')

    payload = json.loads(request.body)

    invalid_fields = helpers.validates_payload(payload)
    if invalid_fields:
        return helpers.error_response(400, 'Bad Request.', invalid_fields)

    if helpers.plan_code_already_exists(payload['plan_code']):
        invalid_fields = [{'plan_code': 'already exists.'}]
        return helpers.error_response(500, 'Internal Server Error.', invalid_fields)

    try:
        plan = Plans(
            plan_code=payload['plan_code'],
            minutes=int(payload['minutes']),
            internet=payload['internet'],
            price=float(payload['price']),
            plan_type=payload['plan_type'].lower(),
            operator=payload['operator'].lower(),
            ddds=payload['ddds']
        )
        plan.save()
    except Exception:
        helpers.error_response(500, 'Internal Server Error')

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
        return helpers.error_response(400, 'Bad Request.')

    plan = helpers.get_plan_or_none(plan_id)
    if not plan:
        return helpers.error_response(404, 'Not Found.')

    payload = json.loads(request.body)

    invalid_fields = helpers.validates_payload_to_update(payload)
    if invalid_fields:
        return helpers.error_response(400, 'Bad Request.', invalid_fields)

    if 'plan_code' in payload and helpers.plan_code_already_exists(payload['plan_code']):
        invalid_fields = [{'plan_code': 'already exists.'}]
        return helpers.error_response(500, 'Internal Server Error.', invalid_fields)

    plan_code = payload['plan_code'] if 'plan_code' in payload else plan.plan_code
    minutes = payload['minutes'] if 'minutes' in payload else plan.minutes
    internet = payload['internet'] if 'internet' in payload else plan.internet
    price = payload['price'] if 'price' in payload else plan.price
    plan_type = payload['plan_type'] if 'plan_type' in payload else plan.plan_type
    operator = payload['operator'] if 'operator' in payload else plan.operator
    ddds = payload['ddds'] if 'ddds' in payload else plan.ddds

    try:
        plan.plan_code=plan_code
        plan.minutes=int(minutes)
        plan.internet=internet
        plan.price=float(price)
        plan.plan_type=plan_type.lower()
        plan.operator=operator.lower()
        plan.ddds=ddds
        plan.save()
    except Exception:
        helpers.error_response(500, 'Internal Server Error')

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
def delete(request, plan_id):
    if not request.method == 'POST':
        return helpers.error_response(400, 'Bad Request.')

    plan = helpers.get_plan_or_none(plan_id)
    if not plan:
        return helpers.error_response(404, 'Not Found.')

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

    try:
        plan.delete()
    except Exception:
        helpers.error_response(500, 'Internal Server Error')

    return JsonResponse(response, status=200)

@csrf_exempt
def list(request):
    if not request.method == 'GET':
        return helpers.error_response(400, 'Bad Request.')

    payload = []
    queryset = dict(request.GET)

    lookups = helpers.build_lookups(queryset)

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
