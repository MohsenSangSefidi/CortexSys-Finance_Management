from django.urls import path
from .views import RegisterAccountView, LoginAccountView, RefreshTokenView, UserInfo

urlpatterns = [
    path("register/", RegisterAccountView.as_view(), name="register"),
    path("login/", LoginAccountView.as_view(), name="login"),
    path('user-info/', UserInfo.as_view(), name='user_info'),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
