from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from website.forms import RepositoryMiceForm
from website.models import Mouse


@login_required
def mice_repository(request):
    mymice = Mouse.objects.all()
    template = loader.get_template("repository/mice_repository.html")
    context = {"mymice": mymice}
    return HttpResponse(template.render(context, request))


@login_required
def add_mouse_to_repository(request):
    if request.method == "POST":
        form = RepositoryMiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("repository/add_mouse_to_repository")
    else:
        form = RepositoryMiceForm()
    return render(
        request, "repository/add_mouse_to_repository.html", {"mice_form": form}
    )
