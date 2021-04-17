from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTrusted(BasePermission):
    """Allows access only from trusted source"""
    def has_permission(self, request, view):
        return request.is_trusted


class IsTrustedOrReadOnly(BasePermission):
    """Only allows 'safe' request from untrusted source"""
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.is_trusted
        )