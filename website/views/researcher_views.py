from itertools import chain

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from website.filters import ProjectFilter
from website.forms import CommentForm, MouseSelectionForm
from website.models import Cage, Comment, Mice, Project, Request


@login_required
def researcher_dashboard(request):
    myprojects = Project.objects.all()
    mymice = Mice.objects.all()

    # Update mice counts of each project - inefficient n^m time
    # Should be made a Project or Mice object method instead
    for project in myprojects:
        for mouse in mymice:
            if project.projectname == mouse.project.projectname:
                project.mice_count += 1

    template = loader.get_template("researcher/researcher_dashboard.html")
    context = {
        # Could add researcher/user variable here
        "myprojects": myprojects,
    }
    return HttpResponse(template.render(context, request))


@login_required
def show_project(http_request, projectname):
    myproject = Project.objects.get(pk=projectname)

    # Load page with no "Add Request" form submission
    if http_request.method == "GET":
        mycomment = Comment.objects.all()
        mycage = Cage.objects.all()

        # Select only those mice that belong to this project
        mymice = Mice.objects.select_related("cage").filter(project=projectname)

        # Select all mice that belong to this project that have a request
        queryset_miceids = chain(
            *[
                mymice.filter(id__in=request.mice.all())
                for request in Request.objects.all()
            ]
        )
        mice_ids_with_requests = []
        for mouse in queryset_miceids:
            mice_ids_with_requests.append(mouse.id)

        # Was the search or cancel filter button pressed?
        filter = ProjectFilter(http_request.GET, queryset=mymice)
        if "search" in http_request.GET:
            mymice = filter.qs
        elif "cancel" in http_request.GET:
            filter = ProjectFilter(queryset=mymice)

        template = loader.get_template("researcher/researcher_show_project.html")
        context = {
            "myproject": myproject,
            "mymice": mymice,
            "mycage": mycage,
            "mycomment": mycomment,
            "mice_ids_with_requests": mice_ids_with_requests,
            "projectname": projectname,
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
                "researcher/researcher_show_project.html",
                {"form": form, "projectname": projectname},
            )
    return render(http_request, "add_request.html", {"projectname": projectname})


@login_required
def show_comment(request, mouse_id):
    comment = Comment.objects.get(pk=mouse_id)
    mouse = Mice.objects.get(pk=mouse_id)
    projectname = mouse.project.projectname
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("show_project", projectname=projectname)
    else:
        form = CommentForm(instance=comment)
    return render(
        request, "popups/comment_fragment.html", {"form": form, "comment": comment}
    )
