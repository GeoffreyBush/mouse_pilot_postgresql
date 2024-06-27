from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from mice_repository.models import Mouse
from mice_requests.forms import ClipForm, CullForm, RequestForm
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
        selected_mice_pks = http_request.session.get("selected_mice", [])
        selected_mice = Mouse.objects.filter(pk__in=selected_mice_pks)
        form = RequestForm(initial={"mice": selected_mice})
    return render(
        http_request, "add_request.html", {"form": form, "project_name": project_name}
    )


@login_required
def edit_request(http_request, request_id):
    mice_request = Request.objects.get(pk=request_id)
    if http_request.method == "POST":
        form = RequestForm(http_request.POST, instance=mice_request)
        if form.is_valid():
            form.save()
            return redirect("mice_requests:show_requests")
    else:
        form = RequestForm(instance=mice_request)
    return render(
        http_request, "edit_request.html", {"form": form, "request": mice_request}
    )


@login_required
def delete_request(http_request, request_id):
    mice_request = Request.objects.get(pk=request_id)
    mice_request.delete()
    return redirect("mice_requests:show_requests")


# Refactor this view
@method_decorator(login_required, name="dispatch")
class ConfirmRequestView(View):

    def get(self, http_request, request_id):
        mice_request = Request.objects.get(pk=request_id)
        match mice_request.task_type:
            case "Clip":
                form = ClipForm()
            case "Cull":
                form = CullForm()
            case _:
                pass
        return render(
            http_request,
            "confirm_request.html",
            {"form": form, "request": mice_request},
        )

    def post(self, http_request, request_id):
        mice_request = Request.objects.get(pk=request_id)
        match mice_request.task_type:
            case "Clip":
                form = ClipForm(http_request.POST)
                if form.is_valid():
                    earmark = form.cleaned_data["earmark"]
                    mice_request.confirm(earmark)
            case "Cull":
                form = CullForm(http_request.POST)
                if form.is_valid():
                    culled_date = form.cleaned_data["culled_date"]
                    mice_request.confirm(date=culled_date)
            case _:
                pass

        return redirect("mice_requests:show_requests")
