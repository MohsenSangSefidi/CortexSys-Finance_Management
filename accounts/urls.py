from django.urls import path
from .views import RegisterAccountView, LoginAccountView, RefreshTokenView

urlpatterns = [
    path("register/", RegisterAccountView.as_view(), name="register"),
    path("login/", LoginAccountView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
