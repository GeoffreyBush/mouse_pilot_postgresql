from django.urls import path

from mice_requests import views
from mice_requests.views import ConfirmRequestView

app_name = "mice_requests"

urlpatterns = [
    path("mice_requests:show_requests", views.show_requests, name="show_requests"),
    path(
        "mice_requests:confirm_request/<int:request_id>/",
        ConfirmRequestView.as_view(),
        name="confirm_request",
    ),
    path(
        "mice_requests:add_request/<str:project_name>/",
        views.add_request,
        name="add_request",
    ),
    # Request messaging is not implemented yet
    path("show_message/<int:request_id>/", views.show_message, name="show_message"),
]
