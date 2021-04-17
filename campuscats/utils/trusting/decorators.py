from functools import wraps
from django.http import HttpResponseForbidden
from django.core.exceptions import ImproperlyConfigured
from .verifier import is_trusted


def trusted_required(func):
    """Decorator for views that only allow request from trusted source
    
    Return a `HttpResponseForbidden` instance on fail
    `utils.trusting.TrustingMiddleware` required
    """

    @wraps(func)
    def _wrapped_view(request, *args, **kwargs):
        if request.is_trusted:
            return func(request)
        return HttpResponseForbidden()
    return _wrapped_view
        