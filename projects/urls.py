from django.urls import path

from projects import views
from projects.views import ShowProjectView

app_name = "projects"

urlpatterns = [
    path("add_new_project", views.add_new_project, name="add_new_project"),
    path("list_projects", views.list_projects, name="list_projects"),
    path(
        "show_project/<str:project_name>/",
        ShowProjectView.as_view(),
        name="show_project",
    ),
]
