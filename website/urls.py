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


# if DEBUG is true
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
