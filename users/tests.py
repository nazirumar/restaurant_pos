from django.test import TestCase
from .models import User
from tenants.models import Tenant

class UserModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test', subdomain='test')

    def test_create_user(self):
        user = User.objects.create_user(username='test', password='pass', tenant=self.tenant)
        self.assertEqual(user.tenant, self.tenant)