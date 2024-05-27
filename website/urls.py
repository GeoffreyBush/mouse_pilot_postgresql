from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import *  # noqa: F403

# Unsorted URLs
urlpatterns = [
    path(
        "", views.mice_repository, name="mice_repository"
    ),  # dashboard is placeholder, should probably be a login or home page instead
    path("edit_history", views.edit_history, name="edit_history"),
]

# Mice repository URLs
urlpatterns += [
    path("mice_repository", views.mice_repository, name="mice_repository"),
    path(
        "add_mouse_to_repository",
        views.add_mouse_to_repository,
        name="add_mouse_to_repository",
    ),
]

# Researcher URLs
urlpatterns += [
    path("list_projects", views.list_projects, name="list_projects"),
    path("show_project/<str:project_name>/", views.show_project, name="show_project"),
    path("show_project/<str:project_name>/", views.show_project, name="show_project"),
]

# Breeding Cage URLs
urlpatterns += [
    path(
        "list_breeding_cages",
        views.list_breeding_cages,
        name="list_breeding_cages",
    ),
    path("add_breeding_cage", views.add_breeding_cage, name="add_breeding_cage"),
    path(
        "view_breeding_cage<str:box_no>",
        views.view_breeding_cage,
        name="view_breeding_cage",
    ),
    path(
        "edit_breeding_cage<str:box_no>",
        views.edit_breeding_cage,
        name="edit_breeding_cage",
    ),
]

# Add, Edit, and Delete Mouse URLs
urlpatterns += [
    path(
        "add_preexisting_mouse_to_project/<str:project_name>/",
        views.add_preexisting_mouse_to_project,
        name="add_preexisting_mouse_to_project",
    ),
    path(
        "edit_mouse/<str:project_name>/<str:tube>/",
        views.edit_mouse,
        name="edit_mouse",
    ),
    path(
        "delete_mouse/<str:project_name>/<str:tube>/",
        views.delete_mouse,
        name="delete_mouse",
    ),
]

# Request Task URLs
urlpatterns += [
    path("show_requests", views.show_requests, name="show_requests"),
    path(
        "confirm_request/<int:request_id>/",
        views.confirm_request,
        name="confirm_request",
    ),
    path("add_request/<str:project_name>/", views.add_request, name="add_request"),
    # Request messaging is not implemented yet
    path("show_message/<int:request_id>/", views.show_message, name="show_message"),
]

# Login URLs
urlpatterns += [path("signup/", SignUpView.as_view(), name="signup")]  # noqa: F405

# if DEBUG is true
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
