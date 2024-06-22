from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from strain.forms import StrainForm


@login_required
def strain_management(request):
    context = {"strains": StrainForm.Meta.model.objects.all()}
    return render(request, "strain_management.html", context)


@login_required
def add_strain(request):
    if request.method == "POST":
        form = StrainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("strain:strain_management")
    form = StrainForm()
    return render(request, "add_strain.html", {"form": form})
