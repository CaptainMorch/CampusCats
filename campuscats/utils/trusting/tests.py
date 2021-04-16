from ipaddress import IPv4Address, IPv4Network
from django.test import TestCase, override_settings
from django.http import HttpRequest

from user.models import User
from .verifier import is_email_trusted, is_group_trusted, is_network_trusted
from .parser import parse_trusted_networks_setting
from . import is_trusted, TrustingMiddleware


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


class TrustingFunctionsTestCase(TestCase):
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
        request.user = User(email='notallowed@example2.edu.cn')
        self.assertFalse(is_email_trusted(request))

        request.user.email = 'allowed@example.edu.cn'
        self.assertTrue(is_email_trusted(request))

        request.user.is_active = False
        self.assertFalse(is_email_trusted(request))

    @override_settings(**SETTING)
    def test_network(self):
        request = HttpRequest()
        request.META = {'REMOTE_ADDR': '0.0.0.1'}
        self.assertTrue(is_network_trusted(request))

        request.META['REMOTE_ADDR'] = '1.1.1.1'
        self.assertTrue(is_network_trusted(request))

        request.META['REMOTE_ADDR'] = '1.0.0.0'
        self.assertFalse(is_network_trusted(request))


@override_settings(TRUSTING_FUNCTION='utils.trusting.trust_only_staff')
class TrustingMiddlewareTestCase(TestCase):
    def do_nothing(self, request):
        return request

    def test_middleware(self):
        request = HttpRequest()
        request.user = User()
        processed = TrustingMiddleware(self.do_nothing)(request)

        self.assertIs(processed.is_trusted, False)

        processed.user.is_staff = True
        # cached, still False
        self.assertIs(processed.is_trusted, False)

        processed.__dict__.pop('is_trusted')
        self.assertIs(processed.is_trusted, True)
