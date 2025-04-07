from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Item

class UserTestCase(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')

class ItemTestCase(TestCase):
    def test_create_item(self):
        item = Item.objects.create(name='Test Item', description='Test Description')
        self.assertEqual(item.name, 'Test Item')