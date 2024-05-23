from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from website.filters import BWFilter
from website.forms import CageForm, MiceForm
from website.models import Cage, Mice, Strain


@login_required
def list_breeding_cages(request):
    mycages = Cage.objects.all()
    template = loader.get_template("breeding_wing/list_breeding_cages.html")
    context = {"mycages": mycages}
    return HttpResponse(template.render(context, request))


@login_required
def breeding_wing_view_strain(request, strain_name):
    mystrain = Strain.objects.get(strain_name=strain_name)
    mymice = Mice.objects.filter(strain=strain_name).values()
    template = loader.get_template("breeding_wing/breeding_wing_view_strain.html")
    context = {
        "mystrain": mystrain,
        "mymice": mymice,
    }
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
def breeding_wing_view_cage(request, cageID):
    mycage = Cage.objects.get(cageID=cageID)
    mymice = Mice.objects.filter(cage=cageID).values()
    # Select only those mice that belong to this cage
    filter = BWFilter(request.GET, queryset=mymice)
    if "search" in request.GET:
        mymice = filter.qs
    elif "cancel" in request.GET:
        filter = BWFilter(queryset=mymice)
    template = loader.get_template("breeding_wing/breeding_wing_view_cage.html")
    context = {
        "mycage": mycage,
        "mymice": mymice,
        "filter": filter,
    }

    return HttpResponse(template.render(context, request))


@login_required
def create_breeding_pair(request):
    if request.method == "POST":
        form = CageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_breeding_cages")
    else:
        form = CageForm()
    return render(request, "breeding_wing/create_breeding_pair.html", {"form": form})


@login_required
def edit_cage(request, cageID):
    cage = Cage.objects.get(cageID=cageID)
    if request.method == "POST":
        form = CageForm(request.POST, instance=cage)
        if form.is_valid():
            form.save()
            return redirect("list_breeding_cages")
    else:
        form = CageForm(instance=cage)
    return render(request, "edit_cage.html", {"form": form})
