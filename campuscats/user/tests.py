from django.test import TestCase, override_settings, Client
from django.urls import path
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth import get_user_model
from .views import SessionLoginView


@override_settings(ROOT_URLCONF='user.urls')
class SessionLoginViewTestCase(TestCase):
    URL = '/session-login/'
    USERNAME = 'test_user'
    PASSWORD = 'testpwdpwd123'
    post_data = {'username': USERNAME, 'password': PASSWORD}

    def setUp(self):
        get_user_model().objects.create_user(
            self.USERNAME, password=self.PASSWORD)

    def test_success(self):
        response = self.client.post(
            self.URL, self.post_data, content_type='application/json')
        self.assertDictEqual(response.json(), {})

    def test_fail(self):
        data = self.post_data.copy()
        data['password'] = 'fasjfask'
        response = self.client.post(
            self.URL, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        res_obj = response.json()
        non_field_errors = res_obj.pop(NON_FIELD_ERRORS)
        self.assertDictEqual(res_obj, {})
        self.assertEqual(len(non_field_errors), 1)

        err = non_field_errors[0]
        self.assertIn('message', err)
        self.assertEqual(err['code'], 'invalid_login')


@override_settings(ROOT_URLCONF='user.urls')
class CSRFTokenViewTestCase(TestCase):
    LOGIN_URL = '/session-login/'
    CSRF_URL = '/csrf-token/'

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_csrf_fail(self):
        """make sure csrf protection is properly set"""
        response = self.client.post(
            self.LOGIN_URL, {}, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_csrf_set(self):
        self.client.get(self.CSRF_URL)
        self.assertIn('csrftoken', self.client.cookies)

        csrftoken = self.client.cookies['csrftoken'].value
        # headers sent here should be converted to CGI format, so
        # `X-CSRFToken` ends in `HTTP_X_CSRFTOKEN`
        # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.Client.get
        headers = {'HTTP_X_CSRFTOKEN': csrftoken}
        response = self.client.post(self.LOGIN_URL, **headers)
        self.assertEqual(response.status_code, 400)
