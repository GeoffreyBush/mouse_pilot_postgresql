from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def strain_management(request):
    return render(request, "strain_management.html")
