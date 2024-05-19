from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from website.forms import RequestForm
from website.models import Project, Request


@login_required
def show_requests(http_request):
    requests = Request.objects.all()
    return render(http_request, "show_requests.html", {"requests": requests})


@login_required
def add_request(http_request, projectname):
    # Find associated project, if it exists
    project = None
    if projectname is not None:
        project = Project.objects.get(pk=projectname)

    # Fetch RequestForm
    if http_request.method == "POST":
        form = RequestForm(http_request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            task.mice.set(form.cleaned_data["mice"])
            return redirect("show_project", projectname=projectname)
    else:
        form = RequestForm(project=project)
    return render(
        http_request, "add_request.html", {"form": form, "projectname": projectname}
    )


@login_required
def confirm_request(http_request, request_id):
    req = Request.objects.get(pk=request_id)
    req.confirm()
    return redirect("show_requests")


# This show_message view doesn't work currently - no popup renders on show_request.html
@login_required
def show_message(request):

    context = {}
    return render(request, "popups/request_fragment.html", context)
