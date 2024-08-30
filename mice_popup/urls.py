from django.urls import path

from mice_popup import views

app_name = "mice_popup"

urlpatterns = [
    path("family_tree/<str:mouse_pk>/", views.family_tree, name="family_tree"),
]
