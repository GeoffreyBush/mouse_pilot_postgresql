from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # Create a test for this blank url
    path("", RedirectView.as_view(url="mice_repository/", permanent=True)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("breeding_cage/", include("breeding_cage.urls", namespace="breeding_cage")),
    path("mice_popup/", include("mice_popup.urls", namespace="mice_popup")),
    path(
        "mice_repository/", include("mice_repository.urls", namespace="mice_repository")
    ),
    path("mice_requests/", include("mice_requests.urls", namespace="mice_requests")),
    path("projects/", include("projects.urls", namespace="projects")),
    path("stock_cage/", include("stock_cage.urls", namespace="stock_cage")),
    path("strain/", include("strain.urls", namespace="strain")),
    path("system_users/", include("system_users.urls", namespace="system_users")),
    path("wean_pups/", include("wean_pups.urls", namespace="wean_pups")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
