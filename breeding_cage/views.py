from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from breeding_cage.forms import BreedingCageForm, TransferToStockForm
from breeding_cage.models import BreedingCage


@login_required
def list_breeding_cages(request):
    mycages = BreedingCage.objects.all()
    template = loader.get_template("list_breeding_cages.html")
    context = {"mycages": mycages}
    return HttpResponse(template.render(context, request))


@login_required
def view_breeding_cage(request, box_no):
    mycage = BreedingCage.objects.get(box_no=box_no)
    template = loader.get_template("view_breeding_cage.html")
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
            return redirect("breeding_cage:list_breeding_cages")
    else:
        form = BreedingCageForm()
    return render(request, "add_breeding_cage.html", {"form": form})


@login_required
def edit_breeding_cage(request, box_no):
    cage = BreedingCage.objects.get(box_no=box_no)
    if request.method == "POST":
        form = BreedingCageForm(request.POST, instance=cage)
        if form.is_valid():
            form.save()
            return redirect("breeding_cage:list_breeding_cages")
    else:
        form = BreedingCageForm(instance=cage)
    return render(request, "edit_breeding_cage.html", {"form": form})


@login_required
def transfer_to_stock_cage(request, box_no):
    cage = BreedingCage.objects.get(box_no=box_no)
    if request.method == "POST":
        form = TransferToStockForm(request.POST, instance=cage)
        if form.is_valid():
            form.save()
            return redirect("breeding_cage:list_breeding_cages")
    else:
        form = TransferToStockForm(instance=cage)
    return render(request, "transfer_to_stock_cage.html", {"form": form})