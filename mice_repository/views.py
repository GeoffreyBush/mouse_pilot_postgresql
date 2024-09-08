from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.template.response import TemplateResponse

from main.filters import MouseFilter
from mice_repository.forms import MouseCommentForm, RepositoryMiceForm
from mice_repository.models import Mouse, MouseComment


@login_required
def mice_repository(request):
    template = loader.get_template("mice_repository.html")
    repository_mice_qs = MouseFilter.get_filtered_mice(
        Mouse.objects.all().order_by("_global_id"),
        request,
    )
    context = {
        "repository_mice_qs": repository_mice_qs,
        "filter_form": MouseFilter.get_filter_form(repository_mice_qs, request),
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_mouse_to_repository(request):
    if request.method == "POST":
        form = RepositoryMiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("mice_repository:mice_repository")
    else:
        form = RepositoryMiceForm()
    return render(request, "add_mouse_to_repository.html", {"form": form})


@login_required
def edit_mouse_in_repository(request, pk):
    mouse = Mouse.objects.get(pk=pk)
    if request.method == "POST":
        form = RepositoryMiceForm(request.POST, instance=mouse)
        if form.is_valid():
            form.save()
            return redirect("mice_repository:mice_repository")
    else:
        form = RepositoryMiceForm(instance=mouse)
    context = {"mouse": mouse, "form": form}
    return TemplateResponse(request, "edit_mouse_in_repository.html", context)


@login_required
def show_mouse_comment(request, pk):
    comment = MouseComment.objects.filter(pk=pk)
    if request.method == "POST":
        form = MouseCommentForm(request.POST, instance=comment.first())
        if form.is_valid():
            form.save()
            # Close comment popup using HTMX on popup window or info panel instead of url redirect
    else:
        if comment.count() == 0:
            form = MouseCommentForm()
        else:
            form = MouseCommentForm(instance=comment.first())
    return render(request, "show_mouse_comment.html", {"form": form})
