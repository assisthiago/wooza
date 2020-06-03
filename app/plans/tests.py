import json

from django.test import TestCase
from django.urls import reverse

from ddt import data, ddt, unpack
from .models import Plans

@ddt
class PlanCreateTestCase(TestCase):
    def setUp(self):
        self.content_type = 'application/json'
        self.payload = {
            'plan_code': 'OiPos10gb100',
            'minutes': 100,
            'internet': '10GB',
            'price': '29.75',
            'plan_type': 'Pós',
            'operator': 'Oi',
            'ddds': [21, 22]
        }

    def tearDown(self):
        Plans.objects.all().delete()

    def test_request_invalid(self):
        response = self.client.get(
            reverse('create'), content_type=self.content_type)

        self.assertContains(
            response,
            b'{"error": {"code": 400, "message": "Bad Request."}}',
            status_code=400
        )
        self.assertEqual(response['content-type'], 'application/json')
        self.assertNotEqual(response.request['REQUEST_METHOD'], 'POST')

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

    def test_create_plan(self):
        response = self.client.post(
            reverse('create'), data=self.payload, content_type=self.content_type)

        data = json.loads(response.content)
        plan = Plans.objects.get(pk=data['data'][0]['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')
        self.assertTrue(plan)
        self.assertEqual(plan.id, data['data'][0]['id'])
        self.assertEqual(plan.plan_code, data['data'][0]['plan_code'])
        self.assertEqual(plan.minutes, data['data'][0]['minutes'])
        self.assertEqual(plan.internet, data['data'][0]['internet'])
        self.assertEqual(float(plan.price), data['data'][0]['price'])
        self.assertEqual(plan.plan_type, data['data'][0]['plan_type'])
        self.assertEqual(plan.operator, data['data'][0]['operator'])
        self.assertEqual(plan.ddds, data['data'][0]['ddds'])

    def test_request_duplicate_plan_code(self):
        self.client.post(reverse('create'), data=self.payload, content_type=self.content_type)

        response = self.client.post(
            reverse('create'), data=self.payload, content_type=self.content_type)

        expected_message = b'{"error": {"code": 500, "message": "Internal Server Error.", "invalid_fields": [{"plan_code": "already exists."}]}}'

        self.assertContains(response, expected_message, status_code=500)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')


@ddt
class PlanUpdateTestCase(TestCase):
    def setUp(self):
        self.content_type = 'application/json'
        self.payload = {
            'plan_code': 'OiPos10gb100',
            'minutes': 100,
            'internet': '10GB',
            'price': '29.75',
            'plan_type': 'Pós',
            'operator': 'Oi',
            'ddds': [21, 22]
        }

    def tearDown(self):
        Plans.objects.all().delete()

    def test_request_invalid(self):
        response = self.client.get(
            reverse('update', args=[1]), content_type=self.content_type)

        self.assertContains(
            response,
            b'{"error": {"code": 400, "message": "Bad Request."}}',
            status_code=400
        )
        self.assertEqual(response['content-type'], 'application/json')
        self.assertNotEqual(response.request['REQUEST_METHOD'], 'POST')
        self.assertNotEqual(response.request['REQUEST_METHOD'], 'PUT')

    def test_plan_not_found(self):
        response = self.client.put(
            reverse('update', args=[1]), content_type=self.content_type)

        self.assertContains(
            response,
            b'{"error": {"code": 404, "message": "Not Found."}}',
            status_code=404
        )
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'PUT')

    @data(
        ('minutes', '100a', 'is not a valid number.'),
        ('price', '100a.90', 'is not a valid number.'),
        ('price', '100a.90', 'is not a valid number.'),
        ('plan_type', 'Limitado', 'is not a valid choice.'),
        ('ddds', [23], 'is not a valid choice.'),
    )
    @unpack
    def test_request_with_invalid_field(self, field, value, message):
        result = self.client.post(
            reverse('create'), data=self.payload, content_type=self.content_type)

        data = json.loads(result.content)
        plan_id = data['data'][0]['id']

        payload = self.payload
        payload[field] = value

        response = self.client.put(
            reverse('update', args=[plan_id]), data=payload, content_type=self.content_type)

        expected_message = '{"error": {"code": 400, "message": "Bad Request.", "invalid_fields": [{"'+field+'": "'+message+'"}]}}'

        self.assertContains(response, expected_message.encode(), status_code=400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'PUT')

    def test_request_duplicate_plan_code(self):
        result = self.client.post(
            reverse('create'), data=self.payload, content_type=self.content_type)

        data = json.loads(result.content)
        plan_id = data['data'][0]['id']

        response = self.client.put(
            reverse('update', args=[plan_id]), data=self.payload, content_type=self.content_type)

        expected_message = b'{"error": {"code": 500, "message": "Internal Server Error.", "invalid_fields": [{"plan_code": "already exists."}]}}'

        self.assertContains(response, expected_message, status_code=500)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'PUT')

    def test_update_plan_with_put_request(self):
        result = self.client.post(
            reverse('create'), data=self.payload, content_type=self.content_type)

        content = json.loads(result.content)
        plan_id = content['data'][0]['id']

        payload = {
            'plan_code': 'TimControle20gb200',
            'minutes': 200,
            'internet': '20GB',
            'price': '99.85',
            'plan_type': 'Controle',
            'operator': 'Tim',
            'ddds': [21, 22, 11]
        }

        response = self.client.put(
            reverse('update', args=[plan_id]), data=payload, content_type=self.content_type)

        data = json.loads(response.content)
        plan = Plans.objects.get(pk=plan_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'PUT')
        self.assertTrue(plan)
        self.assertEqual(plan.id, data['data'][0]['id'])
        self.assertEqual(plan.plan_code, data['data'][0]['plan_code'])
        self.assertEqual(plan.minutes, data['data'][0]['minutes'])
        self.assertEqual(plan.internet, data['data'][0]['internet'])
        self.assertEqual(float(plan.price), data['data'][0]['price'])
        self.assertEqual(plan.plan_type, data['data'][0]['plan_type'])
        self.assertEqual(plan.operator, data['data'][0]['operator'])
        self.assertEqual(plan.ddds, data['data'][0]['ddds'])

    def test_update_plan_with_post_request(self):
        result = self.client.post(
            reverse('create'), data=self.payload, content_type=self.content_type)

        content = json.loads(result.content)
        plan_id = content['data'][0]['id']

        payload = {
            'plan_code': 'TimControle20gb200',
            'minutes': 200,
            'internet': '20GB',
            'price': '99.85',
            'plan_type': 'Controle',
            'operator': 'Tim',
            'ddds': [21, 22, 11]
        }

        response = self.client.post(
            reverse('update', args=[plan_id]), data=payload, content_type=self.content_type)

        data = json.loads(response.content)
        plan = Plans.objects.get(pk=plan_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')
        self.assertTrue(plan)
        self.assertEqual(plan.id, data['data'][0]['id'])
        self.assertEqual(plan.plan_code, data['data'][0]['plan_code'])
        self.assertEqual(plan.minutes, data['data'][0]['minutes'])
        self.assertEqual(plan.internet, data['data'][0]['internet'])
        self.assertEqual(float(plan.price), data['data'][0]['price'])
        self.assertEqual(plan.plan_type, data['data'][0]['plan_type'])
        self.assertEqual(plan.operator, data['data'][0]['operator'])
        self.assertEqual(plan.ddds, data['data'][0]['ddds'])


class PlanDeleteTestCase(TestCase):
    def setUp(self):
        self.content_type = 'application/json'
        self.payload = {
            'plan_code': 'OiPos10gb100',
            'minutes': 100,
            'internet': '10GB',
            'price': '29.75',
            'plan_type': 'Pós',
            'operator': 'Oi',
            'ddds': [21, 22]
        }

    def tearDown(self):
        Plans.objects.all().delete()

    def test_request_invalid(self):
        response = self.client.get(
            reverse('delete', args=[1]), content_type=self.content_type)

        self.assertContains(
            response,
            b'{"error": {"code": 400, "message": "Bad Request."}}',
            status_code=400
        )
        self.assertEqual(response['content-type'], 'application/json')
        self.assertNotEqual(response.request['REQUEST_METHOD'], 'POST')

    def test_plan_not_found(self):
        response = self.client.post(
            reverse('delete', args=[1]), content_type=self.content_type)

        self.assertContains(
            response,
            b'{"error": {"code": 404, "message": "Not Found."}}',
            status_code=404
        )
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')

    def test_delete_plan(self):
        result = self.client.post(
            reverse('create'), data=self.payload, content_type=self.content_type)

        content = json.loads(result.content)
        plan_id = content['data'][0]['id']

        plan_created = Plans.objects.filter(pk=plan_id).exists()

        self.assertTrue(plan_created)

        response = self.client.post(
            reverse('delete', args=[plan_id]), content_type=self.content_type)

        plan_deleted = Plans.objects.filter(pk=plan_id).exists()

        self.assertFalse(plan_deleted)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')


class PlanListTestCase(TestCase):
    def setUp(self):
        self.content_type = 'application/json'
        self.payload = {
            'plan_code': 'OiPos10gb100',
            'minutes': 100,
            'internet': '10GB',
            'price': '29.75',
            'plan_type': 'Pós',
            'operator': 'Oi',
            'ddds': [21, 22]
        }

    def test_request_invalid(self):
        response = self.client.post(
            reverse('list'), content_type=self.content_type)

        self.assertContains(
            response,
            b'{"error": {"code": 400, "message": "Bad Request."}}',
            status_code=400
        )
        self.assertEqual(response['content-type'], 'application/json')
        self.assertNotEqual(response.request['REQUEST_METHOD'], 'GET')
