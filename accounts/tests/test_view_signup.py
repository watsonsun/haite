from django.test import TestCase
# from django.core.urlresolvers import reverse <-- this is deprecated to line below
from django.urls import resolve, reverse
from django.contrib.auth.forms import User
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from ..views import signup
# from django.contrib.auth.forms import UserCreationForm
from ..forms import SignUpForm

s_username = 'root'
s_email = 'ngsengngiap@gmail.com'
s_password = 'password'

class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        User.objects.create_user(username=s_username, email=s_email, password=s_password)
        self.client.login(username=s_username, password=s_password)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm )

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'root',
            'email': 'ngsengngiap@gmail.com',
            'password1': '12345',
            'password2': '12345'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
         self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

