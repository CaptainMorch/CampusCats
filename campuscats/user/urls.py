from django.urls import path
from .views import SessionLoginView, SessionLogoutView, CSRFTokenView


urlpatterns = [
    path('session-login/', SessionLoginView.as_view(), name='session-login'),
    path('session-logout/', SessionLogoutView.as_view(), name='session-logout'),
    path('csrf-token/', CSRFTokenView.as_view(), name='csrf-token'),
]
