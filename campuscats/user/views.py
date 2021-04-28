from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


# Django standard login view is preffered for safety concerns.
# However it dosen't accept json-format data, and don't return json
#
# So first override its responsing behavier by subclassing,
#   than wrap a djrf APIView around it to parse post data.

class WrappedLoginView(LoginView):
    """standard login view that return JsonResponse"""
    
    def form_valid(self, form):
        return JsonResponse({}, status=HTTP_200_OK)

    def form_invalid(self, form):
        data = form.errors.get_json_data()
        return JsonResponse(data, status=HTTP_400_BAD_REQUEST)


class SessionLoginView(APIView):
    """login api view.
    
    required post fields:
      username: str
      password: str
    """
    def post(self, request, *args, **kwargs):
        real_func = WrappedLoginView.as_view()
        # djrf Request is a wrapper instead of a subclass of django Request,
        # so directly passing it to LoginView will trigger AssertError
        django_request = request._request
        data = request.data
        django_request.POST = data
        return real_func(django_request)


class SessionLogoutView(APIView):
    """Logout view for session based auth. POST only"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({}, status=HTTP_200_OK)


class CSRFTokenView(APIView):
    """View that explictly sets csrf cookie to client.
    
    'safe' action, accepts GET only.
    """
    @method_decorator(ensure_csrf_cookie)
    def get(self, *args, **kwargs):
        return Response(status=HTTP_200_OK)
