from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View

from mice_repository.models import Mouse
from projects.filters import ProjectFilter
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


@method_decorator(login_required, name="dispatch")
class ShowProjectView(View):

    # Could add form/template class variables here

    def get(self, http_request, project_name):
        project = Project.objects.get(pk=project_name)
        project_mice = Mouse.objects.filter(project=project_name)
        if "search" in http_request.GET:
            filter = ProjectFilter(http_request.GET, queryset=project_mice)
            project_mice = filter
        else:
            project_mice = ProjectFilter(queryset=project_mice)

        template = loader.get_template("show_project.html")
        context = {
            "project": project,
            "project_mice": project_mice,
        }
        return HttpResponse(template.render(context, http_request))

    def post(self, http_request, project_name):
        project = Project.objects.get(pk=project_name)
        form = MouseSelectionForm(project=project)
        if form.is_valid():
            form.save()
            form.mice.set(form.cleaned_data["mice"])
            return redirect("website:add_request")
        else:
            return render(
                http_request,
                "show_project.html",
                {"form": form, "project_name": project_name},
            )
