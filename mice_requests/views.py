from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from mice_requests.forms import RequestForm
from mice_requests.models import Request


@login_required
def show_requests(http_request):
    requests = Request.objects.all()
    return render(http_request, "show_requests.html", {"requests": requests})


@login_required
def add_request(http_request, project_name):
    if http_request.method == "POST":
        form = RequestForm(http_request.POST)
        if form.is_valid():
            request = form.save(commit=False)
            request.requested_by = http_request.user
            request.save()
            request.mice.set(form.cleaned_data["mice"])
            return redirect("projects:show_project", project_name=project_name)
    else:
        form = RequestForm()
    return render(
        http_request, "add_request.html", {"form": form, "project_name": project_name}
    )


@login_required
def confirm_request(http_request, request_id):
    mice_request = Request.objects.get(pk=request_id)
    # Add switch statement here to check task_type and call appropriate method
    mice_request.confirm_clip("TL") # placeholder earmark
    return redirect("mice_requests:show_requests")


# This show_message view doesn't work currently - no popup renders on show_request.html
@login_required
def show_message(request):

    context = {}
    return render(request, "popups/request_fragment.html", context)
