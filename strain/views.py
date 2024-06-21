from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def strain_management(request):
    return render(request, "strain_management.html")
