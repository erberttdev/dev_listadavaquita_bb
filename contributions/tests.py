from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from events.models import Event
from gifts.models import Gift
from .models import Contribution
from datetime import date

class ContributionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='user@example.com', password='pass1234', username='user1')
        self.event = Event.objects.create(user=self.user, name='Aniversário', date=date.today(), visibility='public')
        self.gift = Gift.objects.create(event=self.event, name='Presente Teste', value=100.00, priority=1)
        self.client.login(email='user@example.com', password='pass1234')

    def test_contribution_creation(self):
        contribution = Contribution.objects.create(
            gift=self.gift,
            name='Contribuinte Teste',
            email='contribuinte@example.com',
            phone='123456789',
            cpf='123.456.789-00',
            amount=50.00,
            message='Boa sorte!',
            payment_status='approved'
        )
        self.assertEqual(contribution.name, 'Contribuinte Teste')
        self.assertEqual(contribution.gift, self.gift)

    def test_contribution_create_view(self):
        url = reverse('contributions:contribute', args=[self.gift.pk])
        data = {
            'name': 'Contribuinte View',
            'email': 'view@example.com',
            'phone': '987654321',
            'cpf': '987.654.321-00',
            'amount': 30.00,
            'message': 'Parabéns!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contribution.objects.filter(name='Contribuinte View').exists())

    def test_contribution_progress_view(self):
        url = reverse('contributions:progress', args=[self.gift.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.gift.name)
