from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View

from main.filters import MouseFilter
from common.forms import MouseSelectionForm
from main.view_utils import get_query_params, paginate_queryset
from mice_repository.models import Mouse
from projects.forms import AddMouseToProjectForm, ProjectForm
from projects.models import Project


@login_required
def list_projects(request):
    return TemplateResponse(
        request, "list_projects.html", {"myprojects": Project.objects.all()}
    )


@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects:list_projects")
    else:
        form = ProjectForm()
    return render(request, "add_project.html", {"form": form})


@login_required
def edit_project(request, project_name):
    project = Project.objects.get(project_name=project_name)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:list_projects")
    else:
        form = ProjectForm(instance=Project.objects.get(project_name=project_name))
    return render(request, "edit_project.html", {"project": project, "form": form})


@login_required
def add_mouse_to_project(request, project_name):
    project = Project.objects.get(project_name=project_name)
    strain_pks = list(project.strains.values_list("pk", flat=True))
    if request.method == "POST":
        form = AddMouseToProjectForm(request.POST, strains=strain_pks)
        if form.is_valid():
            mice = form.cleaned_data["mice"]
            project.mice.add(*mice)
            project.save()
            return redirect("projects:list_projects")
    context = {
        "form": AddMouseToProjectForm(strains=strain_pks),
        "project_name": project_name,
    }
    return render(request, "add_mouse_to_project.html", context)


@method_decorator(login_required, name="dispatch")
class ShowProjectView(View):
    template_name = "show_project.html"
    select_class = MouseSelectionForm
    paginate_by = 10

    def get_project(self, project_name):
        return get_object_or_404(Project, project_name=project_name)

    def get_context(self, http_request, project_name, form_data=None):
        project = self.get_project(project_name)
        mice_qs = MouseFilter.get_filtered_mice(
            Mouse.objects.filter(project=project.pk).order_by("_global_id"),
            http_request,
        )
        project_mice = paginate_queryset(mice_qs, http_request, self.paginate_by)

        return {
            "project": project,
            "project_mice": project_mice,
            "select_form": self.select_class(project=project),
            "filter_form": MouseFilter.get_filter_form(mice_qs, http_request, project),
            "query_params": get_query_params(http_request),
        }

    def get(self, http_request, project_name):
        context = self.get_context(http_request, project_name)
        return render(http_request, self.template_name, context)

    def post(self, http_request, project_name):
        project = self.get_project(project_name)
        select_form = self.select_class(http_request.POST, project=project)
        if select_form.is_valid():
            selected_mice = select_form.cleaned_data["mice"]
            http_request.session["selected_mice"] = [
                mouse.pk for mouse in selected_mice
            ]
            return redirect("mice_requests:add_request", project_name=project_name)
        context = self.get_context(
            http_request, project_name, form_data=http_request.POST
        )
        return render(http_request, self.template_name, context)


@login_required
def info_panel(request, mouse_id):
    mouse = Mouse.objects.get(pk=mouse_id)
    return render(request, "info_panel.html", {"mouse": mouse})
