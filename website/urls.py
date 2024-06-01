from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import mice_repository.views

from . import views

app_name = "website"

# Unsorted URLs
urlpatterns = [
    path(
        "", mice_repository.views.mice_repository, name="mice_repository"
    ),  # dashboard is placeholder, should probably be a login or home page instead
    # path("edit_history", views.edit_history, name="edit_history"),
]


# Add, Edit, and Delete Mouse URLs
urlpatterns += [
    path(
        "website:delete_mouse/<str:project_name>/<str:tube>/",
        views.delete_mouse,
        name="delete_mouse",
    ),
]

# Request Task URLs
urlpatterns += [
    path("website:show_requests", views.show_requests, name="show_requests"),
    path(
        "website:confirm_request/<int:request_id>/",
        views.confirm_request,
        name="confirm_request",
    ),
    path(
        "website:add_request/<str:project_name>/", views.add_request, name="add_request"
    ),
    # Request messaging is not implemented yet
    path("show_message/<int:request_id>/", views.show_message, name="show_message"),
]


# if DEBUG is true
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
