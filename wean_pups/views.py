from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from breeding_cage.models import BreedingCage
from wean_pups.forms import PupsToStockCageForm, PupsToStockCageFormSet


@method_decorator(login_required, name="dispatch")
class PupsToStockCageView(View):
    template_name = "pups_to_stock_cage.html"

    def dispatch(self, request, box_no, *args, **kwargs):
        try:
            self.box_no = box_no
            self.cage = BreedingCage.objects.get(box_no=self.box_no)
            self.MouseFormSet = formset_factory(
                PupsToStockCageForm, formset=PupsToStockCageFormSet, extra=0
            )
        except BreedingCage.DoesNotExist:
            raise Http404("Breeding cage does not exist")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        initial_data = self.cage.get_initial_data_for_pups()
        formset = self.MouseFormSet(initial=initial_data, prefix="mouse")
        return render(request, self.template_name, {"formset": formset})

    def post(self, request):
        formset = self.MouseFormSet(request.POST, prefix="mouse")
        if self.cage.transferred_to_stock:
            formset.non_form_errors().append(
                "Pups have already been transferred out of this breeding cage"
            )
            return render(request, self.template_name, {"formset": formset})
        elif formset.is_valid():
            formset.save(self.cage)
            self.cage.save()
            return redirect("breeding_cage:list_breeding_cages")
        else:
            return render(request, self.template_name, {"formset": formset})
