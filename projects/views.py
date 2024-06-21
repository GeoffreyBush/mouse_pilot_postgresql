from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View

from mice_repository.models import Mouse
from projects.filters import ProjectFilter
from projects.forms import AddMouseToProjectForm, NewProjectForm
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


@login_required
def add_mouse_to_project(request, project_name):
    project = Project.objects.get(project_name=project_name)
    strain_pks = list(project.strains.values_list("pk", flat=True))
    if request.method == "POST":
        form = AddMouseToProjectForm(request.POST, strains=strain_pks)
        print("form.errors", form.errors)
        if form.is_valid():
            mice = form.cleaned_data["mice"]
            print("mice", mice)
            print("*mice", *mice)
            project.mice.add(*mice)
            project.save()
            return redirect("projects:list_projects")
    else:
        form = AddMouseToProjectForm(strains=strain_pks)
    return render(request, "add_mouse_to_project.html", {"form": form, "project_name": project_name})


@method_decorator(login_required, name="dispatch")
class ShowProjectView(View):
    template_name = "show_project.html"
    select_class = MouseSelectionForm
    filter_class = ProjectFilter
    paginate_by = 10

    def filter_project_mice(self, project, http_request):
        project_mice = Mouse.objects.filter(project=project.pk).order_by("_global_id")
        if "search" in http_request.GET:
            filter_form = self.filter_class(http_request.GET, queryset=project_mice)
            project_mice = filter_form.qs
        else:
            filter_form = self.filter_class(queryset=project_mice)
        return project_mice, filter_form

    def paginate_project_mice(self, project_mice, http_request):
        paginator = Paginator(project_mice, self.paginate_by)
        page = http_request.GET.get("page")

        try:
            paginated_mice = paginator.page(page)
        except PageNotAnInteger:
            paginated_mice = paginator.page(1)
        except EmptyPage:
            paginated_mice = paginator.page(paginator.num_pages)

        return paginated_mice

    def get_context(self, http_request, project_name, form_data=None):
        project = Project.objects.get(project_name=project_name)
        project_mice, filter_form = self.filter_project_mice(project, http_request)
        paginated_mice = self.paginate_project_mice(project_mice, http_request)

        if form_data:
            select_form = self.select_class(form_data, project=project)
        else:
            select_form = self.select_class(project=project)

        query_params = http_request.GET.copy()
        if "page" in query_params:
            del query_params["page"]

        context = {
            "project": project,
            "project_mice": paginated_mice,
            "select_form": select_form,
            "filter_form": filter_form,
            "query_params": query_params,
        }
        return context

    def get(self, http_request, project_name):
        context = self.get_context(http_request, project_name)
        return render(http_request, self.template_name, context)

    def post(self, http_request, project_name):
        project = Project.objects.get(project_name=project_name)
        select_form = self.select_class(http_request.POST, project=project)
        if select_form.is_valid():
            selected_mice = select_form.cleaned_data["mice"]
            http_request.session["selected_mice"] = [
                mouse.pk for mouse in selected_mice
            ]
            return redirect("mice_requests:add_request", project_name=project_name)
        else:
            context = self.get_context(
                http_request, project_name, form_data=http_request.POST
            )
            return render(http_request, self.template_name, context)


@login_required
def info_panel(request, mouse_id):
    mouse = Mouse.objects.get(pk=mouse_id)
    return render(request, "info_panel.html", {"mouse": mouse})
