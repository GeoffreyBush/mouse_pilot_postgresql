from django.urls import path

from strain import views

app_name = "strain"

# Unsorted URLs
urlpatterns = [
    path("strain_management", views.strain_management, name="strain_management"),
]
