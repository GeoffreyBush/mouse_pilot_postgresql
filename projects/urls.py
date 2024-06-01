from django.urls import path
from projects import views

app_name = "projects"

urlpatterns = [
    path("list_projects", views.list_projects, name="list_projects"),
    path("show_project/<str:project_name>/", views.show_project, name="show_project"),
]