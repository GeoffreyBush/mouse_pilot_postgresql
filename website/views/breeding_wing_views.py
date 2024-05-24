from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from website.filters import BWFilter
from website.forms import BreedingCageForm, BreedingPairForm, MiceForm
from website.models import BreedingCage, Mice


@login_required
def list_breeding_cages(request):
    mycages = BreedingCage.objects.all()
    template = loader.get_template("breeding_wing/list_breeding_cages.html")
    context = {"mycages": mycages}
    return HttpResponse(template.render(context, request))


@login_required
def breeding_wing_add_litter(request):
    if request.method == "POST":
        form = MiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_breeding_cages")
    else:
        form = MiceForm()
    return render(
        request, "breeding_wing/breeding_wing_add_litter.html", {"form": form}
    )


@login_required
def view_breeding_cage(request, box_no):
    mycage = BreedingCage.objects.get(box_no=box_no)
    template = loader.get_template("breeding_wing/view_breeding_cage.html")
    context = {
        "mycage": mycage,
    }

    return HttpResponse(template.render(context, request))


@login_required
def create_breeding_pair(request):
    if request.method == "POST":
        form = BreedingPairForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_breeding_cages")
    else:
        form = BreedingPairForm()
    return render(request, "breeding_wing/create_breeding_pair.html", {"form": form})


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
    return render(request, "breeding_wing/edit_breeding_cage.html", {"form": form})
