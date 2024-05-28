from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from website.forms import ProjectMiceForm
from mice_repository.models import Mouse


@login_required
def edit_mouse(request, project_name, tube):
    mouse = Mouse.objects.get(pk=tube)
    if request.method == "POST":
        form = ProjectMiceForm(request.POST, instance=mouse)
        if form.is_valid():
            form.save()
            return redirect("show_project", project_name=project_name)
    else:
        form = ProjectMiceForm(instance=mouse)
    return render(
        request, "edit_mouse.html", {"form": form, "project_name": project_name}
    )


@login_required
def add_preexisting_mouse_to_project(request, project_name):
    if request.method == "POST":
        form = ProjectMiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_project", project_name=project_name)
    else:
        form = ProjectMiceForm()
    return render(
        request,
        "researcher/add_preexisting_mouse_to_project.html",
        {"mice_form": form, "project_name": project_name},
    )


@login_required
def delete_mouse(request, project_name, tube):
    mouse = Mouse.objects.get(pk=tube)
    mouse.delete()
    return redirect("show_project", project_name=project_name)


# Edit history is broken by missing tube attribute in mice
"""
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
"""
