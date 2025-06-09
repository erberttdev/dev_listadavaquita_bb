from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from events.models import Event
from gifts.models import Gift
from contributions.models import Contribution
from unittest.mock import patch
from datetime import date
import json

class PaymentsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='user@example.com', password='pass1234', username='user1')
        self.event = Event.objects.create(user=self.user, name='Aniversário', date=date.today(), visibility='public')
        self.gift = Gift.objects.create(event=self.event, name='Presente Teste', value=100.00, priority=1)
        self.contribution = Contribution.objects.create(
            gift=self.gift,
            name='Contribuinte Teste',
            email='contribuinte@example.com',
            phone='123456789',
            cpf='123.456.789-00',
            amount=50.00,
            message='Boa sorte!',
            payment_status='pending'
        )
        self.client = Client()
        self.client.login(email='user@example.com', password='pass1234')

    @patch('mercadopago.SDK.preference')
    def test_create_payment_view(self, mock_preference):
        mock_preference.return_value.create.return_value = {
            "response": {
                "init_point": "http://fakeinitpoint.com"
            }
        }
        url = reverse('payments:create_payment')
        response = self.client.post(url, data=json.dumps({'contribution_id': self.contribution.id}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('init_point', response.json())

    def test_mercadopago_webhook(self):
        url = reverse('payments:mercadopago_webhook')
        payload = {
            "type": "payment",
            "data": {
                "id": "123456"
            }
        }
        response = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
