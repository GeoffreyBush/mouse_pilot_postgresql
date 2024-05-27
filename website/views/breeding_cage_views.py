from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from website.forms import BreedingCageForm, BreedingPairForm
from website.models import BreedingCage


@login_required
def list_breeding_cages(request):
    mycages = BreedingCage.objects.all()
    template = loader.get_template("breeding_cages/list_breeding_cages.html")
    context = {"mycages": mycages}
    return HttpResponse(template.render(context, request))


@login_required
def view_breeding_cage(request, box_no):
    mycage = BreedingCage.objects.get(box_no=box_no)
    template = loader.get_template("breeding_cages/view_breeding_cage.html")
    context = {
        "mycage": mycage,
    }

    return HttpResponse(template.render(context, request))

@login_required
def add_breeding_cage(request):
    if request.method == "POST":
        form = BreedingCageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_breeding_cages")
    else:
        form = BreedingCageForm()
    return render(request, "breeding_cages/add_breeding_cage.html", {"form": form})

@login_required
def edit_breeding_cage(request, box_no):
    cage = BreedingCage.objects.get(box_no=box_no)
    if request.method == "POST":
        form = BreedingCageForm(request.POST, instance=cage)
        if form.is_valid():
            form.save()
            return redirect("list_breeding_cages")
    else:
        form = BreedingCageForm(instance=cage)
    return render(request, "breeding_cages/edit_breeding_cage.html", {"form": form})
