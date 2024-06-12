from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from mice_repository.models import Mouse
from mice_requests.forms import RequestForm, ClipForm, CullForm
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


@method_decorator(login_required, name="dispatch")
# Need an intermediary view here that pops up on the template to offer selection (e.g. earmark is "TL") based on task type
# Then the intermediary view will call the appropriate method to confirm the request or possible redirects here
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
        return render(http_request, "confirm_request.html", {"form": form, "request": mice_request})
    
    def post(self, http_request, request_id):
        pass


# This show_message view doesn't work currently - no popup renders on show_request.html
@login_required
def show_message(request):

    context = {}
    return render(request, "popups/request_fragment.html", context)
