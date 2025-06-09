from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Event
from datetime import date

class EventTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='user@example.com', password='pass1234', username='user1')
        self.client.login(email='user@example.com', password='pass1234')

    def test_event_creation(self):
        event = Event.objects.create(user=self.user, name='Aniversário', date=date.today(), visibility='public')
        self.assertEqual(event.name, 'Aniversário')
        self.assertEqual(event.user, self.user)

    def test_event_list_view(self):
        url = reverse('events:event_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_list.html')

    def test_event_create_view(self):
        url = reverse('events:event_create')
        data = {'name': 'Casamento', 'date': '2024-12-31', 'visibility': 'private'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Event.objects.filter(name='Casamento').exists())

    def test_event_detail_view(self):
        event = Event.objects.create(user=self.user, name='Festa', date=date.today(), visibility='public')
        url = reverse('events:event_detail', args=[event.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Festa')
