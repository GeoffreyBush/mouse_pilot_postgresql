from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from website.forms import ProjectMiceForm
from website.models import HistoricalMouse, Mouse


@login_required
def edit_mouse(request, projectname, mouse_id):
    mouse = Mouse.objects.get(id=mouse_id)
    if request.method == "POST":
        form = ProjectMiceForm(request.POST, instance=mouse)
        if form.is_valid():
            form.save()
            return redirect("show_project", projectname=projectname)
    else:
        form = ProjectMiceForm(instance=mouse)
    return render(
        request, "edit_mouse.html", {"form": form, "projectname": projectname}
    )


@login_required
def add_preexisting_mouse_to_project(request, projectname):
    if request.method == "POST":
        form = ProjectMiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_project", projectname=projectname)
    else:
        form = ProjectMiceForm()
    return render(
        request,
        "researcher/add_preexisting_mouse_to_project.html",
        {"mice_form": form, "projectname": projectname},
    )


@login_required
def delete_mouse(request, projectname, mouse_id):
    mouse = Mouse.objects.get(id=mouse_id)
    mouse.delete()
    return redirect("show_project", projectname=projectname)


@login_required
def edit_history(request):
    histories_with_diff = []
    histories = HistoricalMouse.objects.all().order_by("-history_date")

    for history in histories:
        if hasattr(history, "prev_record") and history.prev_record is not None:
            diff = history.diff_against(history.prev_record)
            changed_fields = [
                (change.field, change.old, change.new) for change in diff.changes
            ]
            history.changed_fields = changed_fields
        else:
            history.changed_fields = []

        histories_with_diff.append(history)

    return render(request, "edit_history.html", {"histories": histories_with_diff})
