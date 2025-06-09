from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            full_name='Test User',
            cpf='123.456.789-00',
            birth_date='1990-01-01',
            username='testuser'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.full_name, 'Test User')
        self.assertEqual(user.cpf, '123.456.789-00')
        self.assertEqual(str(user), 'testuser@example.com')
