from django.urls import path, include

from . import views


USER_URL_PATTERNS = [
    path("create/", views.RegisterUserAPIView.as_view(), name="create-user"),
    path("login/", views.LoginAPIView.as_view(), name="login")
]

PROFILE_URL_PATTERNS = [
    path("get-or-update/", views.ProfileGetOrUpdateAPIView.as_view(), name="profile")
]

urlpatterns = [
    path("user/", include(USER_URL_PATTERNS)),
    path("profile/", include(PROFILE_URL_PATTERNS))
]
