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
