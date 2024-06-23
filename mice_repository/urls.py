from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mice_repository import views

app_name = "mice_repository"

urlpatterns = [
    path("", views.mice_repository, name="mice_repository"),
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

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
