from itertools import chain

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from website.filters import ProjectFilter
from website.forms import MouseSelectionForm
from website.models import Mouse, Project, Request


@login_required
def list_projects(request):
    myprojects = Project.objects.all()
    mymice = Mouse.objects.all()

    # Update mice counts of each project - inefficient n^m time
    # Should be made a Project or Mouse object method instead
    for project in myprojects:
        for mouse in mymice:
            if project.project_name == mouse.project.project_name:
                project.mice_count += 1

    template = loader.get_template("researcher/list_projects.html")
    context = {
        # Could add researcher/user variable here
        "myprojects": myprojects,
    }
    return HttpResponse(template.render(context, request))


@login_required
def show_project(http_request, project_name):
    myproject = Project.objects.get(pk=project_name)

    # Load page with no "Add Request" form submission
    if http_request.method == "GET":

        # Select only those mice that belong to this project
        mymice = Mouse.objects.filter(project=project_name)

        # Select all mice that belong to this project that have a request
        queryset_miceids = chain(
            *[
                mymice.filter(_tube__in=request.mice.all())
                for request in Request.objects.all()
            ]
        )
        mice_ids_with_requests = []
        for mouse in queryset_miceids:
            mice_ids_with_requests.append(mouse.pk)

        # Was the search or cancel filter button pressed?
        filter = ProjectFilter(http_request.GET, queryset=mymice)
        if "search" in http_request.GET:
            mymice = filter.qs
        elif "cancel" in http_request.GET:
            filter = ProjectFilter(queryset=mymice)

        template = loader.get_template("researcher/show_project.html")
        context = {
            "myproject": myproject,
            "mymice": mymice,
            "mice_ids_with_requests": mice_ids_with_requests,
            "project_name": project_name,
            "filter": filter,
        }
        return HttpResponse(template.render(context, http_request))

    # If "Add Request" button is pressed
    if http_request.method == "POST":
        form = MouseSelectionForm(project=myproject)
        if form.is_valid():
            form.save()
            form.mice.set(form.cleaned_data["mice"])
            return redirect("add_request")
        else:
            return render(
                http_request,
                "researcher/show_project.html",
                {"form": form, "project_name": project_name},
            )
    return render(http_request, "add_request.html", {"project_name": project_name})
