from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from stock_cage.forms import StockCageForm
from stock_cage.models import StockCage


@login_required
def list_stock_cages(request):
    cages = StockCage.objects.all()
    return render(request, "list_stock_cages.html", {"cages": cages})


@login_required
def add_stock_cage(request):
    if request.method == "POST":
        form = StockCageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stock_cage:list_stock_cages")
    else:
        form = StockCageForm()
    return render(request, "add_stock_cage.html", {"form": form})
