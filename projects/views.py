from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View

from mice_repository.models import Mouse
from projects.filters import ProjectFilter
from projects.forms import NewProjectForm
from projects.models import Project
from website.forms import MouseSelectionForm
from mice_requests.forms import RequestForm


@login_required
def list_projects(request):
    myprojects = Project.objects.all()
    template = loader.get_template("list_projects.html")
    context = {
        "myprojects": myprojects,
    }
    return HttpResponse(template.render(context, request))


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


@method_decorator(login_required, name="dispatch")
class ShowProjectView(View):

    # Could add form/template class variables here

    def get(self, http_request, project_name):
        project = Project.objects.get(project_name=project_name)
        project_mice = Mouse.objects.filter(project=project.pk)
        if "search" in http_request.GET:
            filter = ProjectFilter(http_request.GET, queryset=project_mice)
            project_mice = filter
        else:
            project_mice = ProjectFilter(queryset=project_mice)

        template = loader.get_template("show_project.html")
        context = {
            "project": project,
            "project_mice": project_mice,
            "mouse_selection_form": MouseSelectionForm(project=project),
        }
        return HttpResponse(template.render(context, http_request))

    def post(self, http_request, project_name):
        if "add_request" in http_request.POST:
            project = Project.objects.get(project_name=project_name)
            mouse_selection_form = MouseSelectionForm(http_request.POST, project=project)
            if mouse_selection_form.is_valid():
                selected_mice = mouse_selection_form.cleaned_data["mice"]
                http_request.session["selected_mice"] = [mouse.pk for mouse in selected_mice]
                return redirect("mice_requests:add_request", project_name=project_name)
            else:
                # This render causes NoReverseMatch error
                return render(
                    http_request,
                    "show_project.html",
                    {"mouse_selection_form": mouse_selection_form, "project_name": project_name},
                )
