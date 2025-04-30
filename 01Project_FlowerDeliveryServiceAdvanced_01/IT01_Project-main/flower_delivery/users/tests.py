from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Profile

User = get_user_model()

class UserViewsTests(TestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.edit_profile_url = reverse('edit_profile')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_register_view(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user, self.user)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_profile_view(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_edit_profile_view(self):

        #Profile.objects.create(user=self.user, address='Test bio')

        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_edit.html')


        response = self.client.post(self.edit_profile_url, {
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName',
            'address': 'Updated email',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.address, 'Updated email')