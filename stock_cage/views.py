from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from stock_cage.models import StockCage


@login_required
def list_stock_cages(request):
    cages = StockCage.objects.all()
    return render(request, "list_stock_cages.html", {"cages": cages})
