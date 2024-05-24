from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render

from website.models import Mouse
from website.forms import ProjectMiceForm

@login_required
def mice_repository(request):
    mymice = Mouse.objects.all()
    template = loader.get_template("general/mice_repository.html")
    context = {"mymice": mymice}
    return HttpResponse(template.render(context, request))

@login_required
def add_preexisting_mouse_to_repository(request):
    if request.method == "POST":
        form = ProjectMiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("general/add_preexisting_mouse_to_repository")
    else:
        form = ProjectMiceForm()
    return render(
        request, "general/add_preexisting_mouse_to_repository.html", {"mice_form": form}
    )