from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserRegisterForm

class SignupRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner_signup_url = reverse('signup', args=['owner_signup'])
        self.customer_signup_url = reverse('signup', args=['customer_signup'])
        self.user_data = {
            'first_name': 'testuser',
            'last_name':'testalst',
            'email': 'testuser@example.com',
            'number':986063121,
            'is_owner':True,
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

    def test_owner_signup(self):
        response = self.client.post(self.owner_signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='testuser', is_owner=True).exists())

    def test_customer_signup(self):
        response = self.client.post(self.customer_signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='testuser', is_owner=False).exists())
        
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user, latitude=1.0, longitude=1.0)
        self.valid_payload = {
            'username': 'testuser',
            'password': 'password',
            'latitude': 1.0,
            'longitude': 1.0,
        }
        self.invalid_payload = {
            'username': 'testuser',
            'password': 'wrongpassword',
            'latitude': 1.0,
            'longitude': 1.0,
        }

    def test_login_view_with_valid_payload(self):
        response = self.client.post(self.login_url, data=self.valid_payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_with_invalid_payload(self):
        response = self.client.post(self.login_url, data=self.invalid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertContains(response, 'Invalid username or password.')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_view_with_already_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
