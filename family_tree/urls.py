from django.urls import path

from family_tree import views

app_name = "family_tree"

urlpatterns = [
    path("family_tree/<str:mouse_pk>/", views.family_tree, name="family_tree"),
]