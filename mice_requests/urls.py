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
    path("mice_requests:edit_request/<int:request_id>/", views.edit_request, name="edit_request"),
    path("mice_requests:delete_request/<int:request_id>/", views.delete_request, name="delete_request")
]
