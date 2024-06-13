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
    template_name = "show_project.html"
    form_class = MouseSelectionForm

    def get_project_mice(self, project, http_request):
        project_mice = Mouse.objects.filter(project=project.pk)
        if "search" in http_request.GET:
            filter = ProjectFilter(http_request.GET, queryset=project_mice)
            project_mice = filter
        else:
            project_mice = ProjectFilter(queryset=project_mice)
        return project_mice

    def get(self, http_request, project_name):
        project = Project.objects.get(project_name=project_name)
        project_mice = self.get_project_mice(project, http_request)
        form = self.form_class(project=project)
        context = {
            "project": project,
            "project_mice": project_mice,
            "form": form,
        }
        return render(http_request, self.template_name, context)

    def post(self, http_request, project_name):
        project = Project.objects.get(project_name=project_name)
        form = self.form_class(http_request.POST, project=project)
        if form.is_valid():
            selected_mice = form.cleaned_data["mice"]
            http_request.session["selected_mice"] = [
                mouse.pk for mouse in selected_mice
            ]
            return redirect("mice_requests:add_request", project_name=project_name)
        else:
            project_mice = self.get_project_mice(project, http_request)
            context = {
                "project": project,
                "form": form,
                "project_mice": project_mice,
            }
            return render(http_request, self.template_name, context)


def htmx_test(request):
    return render(request, "htmx_test.html")


def lazy_project_list(request):
    return render(request, "lazy_project_list.html")
