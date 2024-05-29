from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from stock_cage.forms import TransferToStockCageForm
from breeding_cage.models import BreedingCage


@login_required
def transfer_to_stock_cage(request, box_no):
    cage = BreedingCage.objects.get(box_no=box_no)
    if request.method == "POST":
        form = TransferToStockCageForm(request.POST, instance=cage)
        if form.is_valid():
            form.save()
            return redirect("breeding_cage:list_breeding_cages")
    else:
        form = TransferToStockCageForm(instance=cage)
    return render(request, "transfer_to_stock_cage.html", {"form": form})