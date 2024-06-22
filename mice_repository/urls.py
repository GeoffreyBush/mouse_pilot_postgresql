# Mice repository URLs

from django.urls import path

from mice_repository import views

app_name = "mice_repository"

urlpatterns = [
    path("mice_repository", views.mice_repository, name="mice_repository"),
    path(
        "add_mouse_to_repository",
        views.add_mouse_to_repository,
        name="add_mouse_to_repository",
    ),
    path(
        "edit_mouse_in_repository/<str:pk>",
        views.edit_mouse_in_repository,
        name="edit_mouse_in_repository",
    ),
]
