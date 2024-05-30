from django.urls import path

from system_users.views import SignUpView

app_name = "system_users"

urlpatterns = [path("signup/", SignUpView.as_view(), name="signup")]  # noqa: F405
