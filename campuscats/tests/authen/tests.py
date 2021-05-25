from ipaddress import IPv4Address, IPv4Network

from django.http import HttpRequest, HttpResponseForbidden, request
from django.test import TestCase, override_settings, Client
from django.urls import path
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User, AnonymousUser

from authen.permissions import IsEmailTrusted, InTrustedNetworks, InTrustedGroup, IsMemberOrReadOnly
from authen.utils import parse_trusted_networks_setting


#
# View tests
#

@override_settings(ROOT_URLCONF='authen.urls')
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


@override_settings(ROOT_URLCONF='authen.urls')
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


#
# Permission Tests
#

class ParseTrustedNetworksSettingTestCase(TestCase):
    def test_normal(self):
        SETTING = [
            '0.0.0.1',
            ('0.0.0.0', '0.0.2.255'),
            '0.0.3.0/24',
            ('0.0.4.0', '0.0.4.255'),
            '0.0.0.2',
        ]
        EXPECTED = [IPv4Network('0.0.0.1/32')]\
            + [IPv4Network('0.0.0.0/23')]\
            + [IPv4Network(f'0.0.{i}.0/24') for i in range(2, 5)]\
            + [IPv4Network('0.0.0.2/32')]
        output = parse_trusted_networks_setting(*SETTING)
        self.assertListEqual(output, EXPECTED)

    def test_invalid_address(self):
        self.assertRaisesRegex(
            ValueError, '"0.0.0.666" should be',
            parse_trusted_networks_setting,
            '0.0.0.666')

    def test_invalid_range(self):
        self.assertRaisesRegex(
            ValueError, 'should be a 2-tuple',
            parse_trusted_networks_setting,
            ('0.0.0.0',)
        )

    def test_invalid_range_address(self):
        self.assertRaisesRegex(
            ValueError, 'contains invalid',
            parse_trusted_networks_setting,
            ('0.0.0.666', '0.0.0.1')
        )


class PermissionsTestCase(TestCase):
    SETTING = {
        'TRUSTED_EMAIL_DOMAINS': ['@example.edu.cn', '@example2.edu'],
        'TRUSTED_NETWORKS': parse_trusted_networks_setting(
                ('0.0.0.0', '0.0.0.255'), '1.1.1.1',
            ),
        'TRUSTED_USER_GROUP': 'trusted',
    }
    
    @override_settings(**SETTING)
    def test_email(self):
        request = HttpRequest()
        request.user = get_user_model()(email='notallowed@example2.edu.cn')
        self.assertIs(
            IsEmailTrusted().has_permission(request, None),
            False)

        request.user.email = 'allowed@example.edu.cn'
        self.assertIs(
            IsEmailTrusted().has_permission(request, None),
            True)

        request.user.is_active = False
        self.assertIs(
            IsEmailTrusted().has_permission(request, None),
            False)

    @override_settings(**SETTING)
    def test_network(self):
        request = HttpRequest()
        request.META = {'REMOTE_ADDR': '0.0.0.1'}
        self.assertIs(
            InTrustedNetworks().has_permission(request, None),
            True)

        request.META['REMOTE_ADDR'] = '1.1.1.1'
        self.assertIs(
            InTrustedNetworks().has_permission(request, None),
            True)

        request.META['REMOTE_ADDR'] = '1.0.0.0'
        self.assertIs(
            InTrustedNetworks().has_permission(request, None),
            False)

    @override_settings(**SETTING)
    def test_group(self):
        group = Group.objects.create(name='trusted')
        user = get_user_model().objects.create_user('test')
        request = HttpRequest()
        request.user = user

        self.assertIs(
            InTrustedGroup().has_permission(request, None),
            False)

        user.groups.add(group)
        self.assertIs(
            InTrustedGroup().has_permission(request, None),
            True)

class IsMemberOrReadOnlyTeastCase(TestCase):
    def setUp(self):
        self.member = User()
        self.member.is_staff = True
        self.unauth = AnonymousUser()

    def test_safe(self):
        request = HttpRequest()
        request.method = 'GET'

        request.user = self.unauth
        self.assertIs(
            IsMemberOrReadOnly().has_permission(request, None),
            True,
        )

        request.user = self.member
        self.assertIs(
            IsMemberOrReadOnly().has_permission(request, None),
            True,
        )

    def test_unsafe(self):
        request = HttpRequest()
        request.method = 'POST'

        request.user = self.unauth
        self.assertIs(
            IsMemberOrReadOnly().has_permission(request, None),
            False,
        )
        
        request.user = self.member
        self.assertIs(
            IsMemberOrReadOnly().has_permission(request, None),
            True,
        )