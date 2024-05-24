from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import *  # noqa: F403

# Unsorted URLs
urlpatterns = [
    path(
        "", views.researcher_dashboard, name="researcher_dashboard"
    ),  # dashboard is placeholder, should probably be a login or home page instead
    path("show_comment/<int:mouse_id>/", views.show_comment, name="show_comment"),
    path("edit_history", views.edit_history, name="edit_history"),
    path("family_tree/<int:mouse_id>/", views.family_tree, name="family_tree"),
]

# Researcher URLs
urlpatterns += [
    path(
        "researcher_dashboard", views.researcher_dashboard, name="researcher_dashboard"
    ),
    path("show_project/<str:projectname>/", views.show_project, name="show_project"),
    path("show_project/<str:projectname>/", views.show_project, name="show_project"),
]

# Breeding Wing URLs
urlpatterns += [
    path(
        "list_breeding_cages",
        views.list_breeding_cages,
        name="list_breeding_cages",
    ),
    path(
        "breeding_wing_add_litter",
        views.breeding_wing_add_litter,
        name="breeding_wing_add_litter",
    ),
    path(
        "breeding_wing_view_cage<str:cageID>",
        views.breeding_wing_view_cage,
        name="breeding_wing_view_cage",
    ),
]

# Add and Edit Cage URLs
urlpatterns += [
    path(
        "create_breeding_pair",
        views.create_breeding_pair,
        name="create_breeding_pair",
    ),
    path("edit_cage<str:cageID>", views.edit_cage, name="edit_cage"),
]

# Add, Edit, and Delete Mice URLs
urlpatterns += [
    path("add_mouse/<str:projectname>/", views.add_mouse, name="add_mouse"),
    path(
        "edit_mouse/<str:projectname>/<int:mouse_id>/",
        views.edit_mouse,
        name="edit_mouse",
    ),
    path(
        "delete_mouse/<str:projectname>/<int:mouse_id>/",
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
    path("add_request/<str:projectname>/", views.add_request, name="add_request"),
    # Request messaging is not implemented yet
    path("show_message/<int:request_id>/", views.show_message, name="show_message"),
]

# Login URLs
urlpatterns += [path("signup/", SignUpView.as_view(), name="signup")]  # noqa: F405

# if DEBUG is true
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
