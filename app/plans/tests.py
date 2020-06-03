import json

from django.test import TestCase
from django.urls import reverse

from ddt import data, ddt, unpack

@ddt
class PlanCreateTestCase(TestCase):

    def setUp(self):
        self.content_type = 'application/json'
        self.payload = {
            'plan_code': 'OiPro100',
            'minutes': 100,
            'internet': '10GB',
            'price': '29.75',
            'plan_type': 'Pós',
            'operator': 'Oi',
            'ddds': [21]
        }

    def test_request_invalid(self):
        response = self.client.get(
            reverse('create'), content_type=self.content_type)

        self.assertContains(
            response,
            b'{"error": {"code": 400, "message": "Bad Request."}}',
            status_code=400
        )
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'GET')

    @data(
        'plan_code',
        'minutes',
        'internet',
        'price',
        'plan_type',
        'operator',
        'ddds',
    )
    def test_request_with_empty_field(self, field):
        payload = self.payload
        payload[field] = ''

        response = self.client.post(
            reverse('create'), data=payload, content_type=self.content_type)

        expected_message = '{"error": {"code": 400, "message": "Bad Request.", "invalid_fields": [{"'+field+'": "is empty."}]}}'

        self.assertContains(response, expected_message.encode(), status_code=400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')


    @data(
        ('minutes', '100a', 'is not a valid number.'),
        ('price', '100a.90', 'is not a valid number.'),
        ('price', '100a.90', 'is not a valid number.'),
        ('plan_type', 'Limitado', 'is not a valid choice.'),
        ('ddds', [23], 'is not a valid choice.'),
    )
    @unpack
    def test_request_with_invalid_field(self, field, value, message):
        payload = self.payload
        payload[field] = value

        response = self.client.post(
            reverse('create'), data=payload, content_type=self.content_type)

        expected_message = '{"error": {"code": 400, "message": "Bad Request.", "invalid_fields": [{"'+field+'": "'+message+'"}]}}'

        self.assertContains(response, expected_message.encode(), status_code=400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')
