from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from events.models import Event
from .models import Gift
from datetime import date

class GiftTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='user@example.com', password='pass1234', username='user1')
        self.event = Event.objects.create(user=self.user, name='Aniversário', date=date.today(), visibility='public')
        self.client.login(email='user@example.com', password='pass1234')

    def test_gift_creation(self):
        gift = Gift.objects.create(
            event=self.event,
            name='Presente Teste',
            value=100.00,
            store_name='Loja Teste',
            store_type='online',
            store_address_or_link='http://lojateste.com',
            priority=1,
            allow_simultaneous_contributions=True
        )
        self.assertEqual(gift.name, 'Presente Teste')
        self.assertEqual(gift.event, self.event)

    def test_gift_create_view(self):
        url = reverse('gifts:gift_add')
        data = {
            'event': self.event.id,
            'name': 'Presente View',
            'value': 150.00,
            'store_name': 'Loja View',
            'store_type': 'physical',
            'store_address_or_link': 'http://lojaview.com',
            'priority': 2,
            'allow_simultaneous_contributions': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Gift.objects.filter(name='Presente View').exists())

    def test_gift_detail_view(self):
        gift = Gift.objects.create(
            event=self.event,
            name='Presente Detalhe',
            value=200.00,
            priority=3
        )
        url = reverse('gifts:gift_detail', args=[gift.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Presente Detalhe')

    def test_gift_update_view(self):
        gift = Gift.objects.create(
            event=self.event,
            name='Presente Editar',
            value=250.00,
            priority=4
        )
        url = reverse('gifts:gift_edit', args=[gift.pk])
        data = {
            'name': 'Presente Editado',
            'value': 300.00,
            'store_name': 'Loja Editada',
            'store_type': 'online',
            'store_address_or_link': 'http://lojaeditada.com',
            'priority': 5,
            'allow_simultaneous_contributions': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        gift.refresh_from_db()
        self.assertEqual(gift.name, 'Presente Editado')

    def test_gift_delete_view(self):
        gift = Gift.objects.create(
            event=self.event,
            name='Presente Deletar',
            value=350.00,
            priority=6
        )
        url = reverse('gifts:gift_delete', args=[gift.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Gift.objects.filter(name='Presente Deletar').exists())
