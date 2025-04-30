from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomAuthenticationForm

CustomUser = get_user_model()

# Тесты для models.py

class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            phone='1234567890',
            address='123 Test St, Test City, TC'
        )

    def test_user_creation(self):
        # Проверяем, что пользователь был корректно создан
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password123'))
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.address, '123 Test St, Test City, TC')

    def test_email_unique(self):
        # Проверяем уникальность поля email
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                email='testuser@example.com',
                password='password123'
            )

    def test_str_method(self):
        # Проверяем метод __str__
        self.assertEqual(str(self.user), 'Test')

        # Проверяем метод __str__ если first_name пустое
        self.user.first_name = ''
        self.user.save()
        self.assertEqual(str(self.user), 'No Name')

    def test_username_field(self):
        # Проверяем, что поле username не является обязательным и уникальным
        self.assertEqual(self.user.username, '')

        self.user.username = 'testusername'
        self.user.save()
        self.assertEqual(self.user.username, 'testusername')

        user2 = CustomUser.objects.create_user(
            email='testuser2@example.com',
            password='password123',
            username='testusername'
        )
        self.assertEqual(user2.username, 'testusername')

    def test_required_fields(self):
        # Проверка на то, что обязательное поле для создания пользователя - email
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='password123')

    def test_user_update(self):
        # Проверка обновления пользовательских данных
        self.user.first_name = 'NewTest'
        self.user.save()
        self.assertEqual(self.user.first_name, 'NewTest')


# Тесты для forms.py

CustomUser = get_user_model()

class CustomUserCreationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'phone': '1234567890',
            'address': '123 Test St, Test City, TC',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'phone': '1234567890',
            'address': '123 Test St, Test City, TC',
            'password1': 'password123',
            'password2': 'differentpassword'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_required_fields(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

class CustomAuthenticationFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password123'
        )

    def test_valid_authentication(self):
        form_data = {
            'username': 'testuser@example.com',
            'password': 'password123'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_authentication(self):
        form_data = {
            'username': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('non_field_errors', form.errors)

    def test_username_field_label(self):
        form = CustomAuthenticationForm()
        self.assertEqual(form.fields['username'].label, 'Email')
        self.assertEqual(form.fields['username'].max_length, 254)
        self.assertTrue(isinstance(form.fields['username'].widget, form.EmailInput))

# Тесты для views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
        }
        self.existing_user = CustomUser.objects.create_user(username='existinguser', email='existing@example.com', password='password123')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_view_post_success(self):
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(CustomUser.objects.filter(email=self.user_data['email']).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Регистрация прошла успешно!')

    def test_register_view_post_user_exists(self):
        data = self.user_data.copy()
        data['email'] = self.existing_user.email
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertFormError(response, 'form', 'email', 'Пользователь с таким email уже существует.')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Пользователь с таким email уже существует.')

class CustomLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='password123')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': 'password123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('flowers'))  # Предполагается, что URL 'flowers' существует

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')


# Тесты для urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import register, CustomLoginView


class URLTests(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_register_url_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_url_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)