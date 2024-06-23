from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View

from mice_repository.models import Mouse
from mouse_pilot_postgresql.filters import MouseFilter
from mouse_pilot_postgresql.view_utils import get_query_params, paginate_queryset
from projects.forms import AddMouseToProjectForm, NewProjectForm
from projects.models import Project
from website.forms import MouseSelectionForm


@login_required
def list_projects(request):
    return TemplateResponse(
        request, "list_projects.html", {"myprojects": Project.objects.all()}
    )


@login_required
def add_new_project(request):
    if request.method == "POST":
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects:list_projects")
    else:
        form = NewProjectForm()
    return render(request, "add_new_project.html", {"form": form})


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
    filter_class = MouseFilter
    paginate_by = 10

    def get_project(self, project_name):
        return get_object_or_404(Project, project_name=project_name)

    def get_select_form(self, project, form_data=None):
        if form_data:
            return self.select_class(form_data, project=project)
        return self.select_class(project=project)

    def get_context(self, http_request, project_name, form_data=None):
        project = self.get_project(project_name)
        mice_qs = Mouse.objects.filter(project=project.pk).order_by("_global_id")
        project_mice = MouseFilter.get_filtered_mice(mice_qs, http_request)
        filter_form = MouseFilter.get_filter_form(mice_qs, http_request)
        paginated_mice = paginate_queryset(project_mice, http_request, self.paginate_by)
        select_form = self.get_select_form(project, form_data)

        return {
            "project": project,
            "project_mice": paginated_mice,
            "select_form": select_form,
            "filter_form": filter_form,
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
