from django.shortcuts import render


def strain_management(request):
    return render(request, "strain_management.html")
