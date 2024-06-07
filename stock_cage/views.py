from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import redirect, render

from breeding_cage.models import BreedingCage
from stock_cage.forms import BatchFromBreedingCageForm
from stock_cage.models import StockCage


@login_required
def list_stock_cages(request):
    cages = StockCage.objects.all()
    return render(request, "list_stock_cages.html", {"cages": cages})


