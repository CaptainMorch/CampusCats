from ipaddress import IPv4Address
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.permissions import (
    BasePermission, IsAdminUser, AllowAny, SAFE_METHODS)


class IsEmailTrusted(BasePermission):
    """
    Allow requests from users with activated email of trusted domains.
    Not for directly using
    """
    def has_permission(self, request, view):
        user = request.user
        # user not verified is 'authenticated' but not 'active'
        if user.is_authenticated and user.is_active and any(
                user.email.endswith(domain)
                for domain in settings.TRUSTED_EMAIL_DOMAINS):
            return True
        return False

class InTrustedNetworks(BasePermission):
    """
    Allow requests from ip in trusted networks.
    Not for directly using
    """
    def has_permission(self, request, view):
        address = IPv4Address(request.META['REMOTE_ADDR'])
        networks = settings.TRUSTED_NETWORKS
        return any(address in network for network in networks)

class InTrustedGroup(BasePermission):
    """
    Allow requests from users in trusted group.
    Not for directly using
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_active and user.groups.filter(
                name=settings.TRUSTED_USER_GROUP).exists()

class IsMemberOrReadOnly(IsAdminUser):
    """
    Block anyone excepts members from accessing 'dangerous' methods
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)
        
        
#
# Permissions for using in settings
#
# AllowAny = AllowAny 
MemebersOnly = IsAdminUser
TrustByEmail = MemebersOnly or IsEmailTrusted
TrustByNetwork = MemebersOnly or InTrustedNetworks
TrustByEmailNetwork = TrustByEmail or InTrustedNetworks
TrustByEmailNetworkGroup = TrustByEmailNetwork or InTrustedGroup


def get_locations_permission():
    setting_field = 'PERMISSION_FOR_VIEWING_LOCATIONS'
    return import_string(getattr(settings, setting_field))

def get_permission():
    setting_field = 'PERMISSION_FOR_NON_SENSITIVE_ACTIONS'
    return import_string(getattr(settings, setting_field))