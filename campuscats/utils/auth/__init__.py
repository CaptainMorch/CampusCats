import ipaddress
from django.utils.module_loading import import_string
from django.conf import settings


def parse_trusted_networks_setting(setting):
    """parse the setting to a list of IPv4Network"""
    domains = []
    for entry in setting:
        if isinstance(entry, str):
            # should represent network or ip address.
            # sigle ip address will be convert to a sigle-address network
            try:
                network = ipaddress.IPv4Network(entry)
            except ipaddress.AddressValueError:
                raise ValueError(f'"{entry}" should be a string '
                    'representing an IPv4 Address or IPv4 Network.')
            else:
                domains.append(network)
                continue

        # must be a 2-tuple representing network
        try:
            ip_start, ip_end = entry
        except ValueError:
            raise ValueError(f'"{entry}" should be a 2-tuple')

        try:
            ip_start = ipaddress.IPv4Address(ip_start)
            ip_end = ipaddress.IPv4Address(ip_end)
        except ipaddress.AddressValueError:
            raise ValueError(f'{entry} contains invalid IPv4 address')

        # the default exception massage is clear enough
        networks_iter = ipaddress.summarize_address_range(
            ip_start, ip_end)

        for network in networks_iter:
            domains.append(network)
    return domains


def is_email_trusted(request):
    user = request.user
    # user not verified is 'authenticated' but not 'active'
    if user.is_authenticated and user.is_active and any(
            user.email.endswith(domain)
            for domain in settings.TRUSTED_EMAIL_DOMAINS):
        return True
    return False

def is_network_trusted(request):
    address = ipaddress.IPv4Address(request.META['REMOTE_ADDR'])
    networks = parse_trusted_networks_setting(settings.TRUSTED_NETWORKS)
    return any(address in network for network in networks)

def is_group_trusted(request):
    user = request.user
    return user.is_active and user.groups.filter(
            name=settings.TRUSTED_USER_GROUP).exists()


# Functions ready to be used in settings
def trust_only_staff(request):
    """same rule as admin site"""
    # user.is_active is not enforced here
    return request.user.is_staff

def trust_all(request):
    """same rule as public api, i.e. no limitations"""
    return True

def trust_by_network_email(request):
    """Trust staffs and users with trusted verified email,
    or from trusted network"""
    return any(
        trust_only_staff(request),
        is_network_trusted(request),
        is_email_trusted(request),
    )

def trust_by_network_email_group(request):
    """Trust staffs and users with trusted verified email,
    or in trusted network or group"""
    return any(
        trust_by_network_email(request),
        is_group_trusted(request),
    )


# Entry function for application code
def is_trusted(request):
    """Determin whether a request is trusted according to your setting"""
    # use cached value if exists
    if hasattr(request, 'is_trusted'):
        return request.is_trusted

    trusting_function = import_string(settings.TRUSTING_FUNCTION)
    trusted = trusting_function(request)
    request.is_trusted = trusted    # cache the value
    return trusted