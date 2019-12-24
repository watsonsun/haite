from django.test import TestCase
# from django.core.urlresolvers import reverse <-- this is deprecated to line below
from django.urls import resolve, reverse
from django.contrib.auth.forms import User
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from ..views import signup
# from django.contrib.auth.forms import UserCreationForm
from ..forms import SignUpForm


class SignUpFormTests(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)