from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("system_users/", include("system_users.urls", namespace="system_users")),
    path("website/", include("website.urls")),
    path("breeding_cage/", include("breeding_cage.urls", namespace="breeding_cage")),
    path("stock_cage/", include("stock_cage.urls", namespace="stock_cage")),
    path(
        "mice_repository/", include("mice_repository.urls", namespace="mice_repository")
    ),
    path("", RedirectView.as_view(url="website/", permanent=True)),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
