from django.utils.functional import cached_property
from .verifier import is_trusted


class TrustingMiddleware:
    """Add property `is_trusted` to request
    
    Depends on django auth system, so put this after django auth middleware
    """
    PROPERTY_NAME = 'is_trusted'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # `is_trusted` accepts one argument `request`, which is sytactically
        # identical to zero-argument method `is_trusted` of Request instance
        descr = cached_property(is_trusted)
        # need to add descriptor to created class
        # https://docs.python.org/3/reference/datamodel.html#object.__set_name__
        setattr(request.__class__, self.PROPERTY_NAME, descr)
        descr.__set_name__(request.__class__, self.PROPERTY_NAME)

        response = self.get_response(request)
        return response