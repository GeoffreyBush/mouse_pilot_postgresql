from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from breeding_cage.models import BreedingCage
from wean_pups.forms import BatchFromBreedingCageForm


@method_decorator(login_required, name="dispatch")
class PupsToStockCageView(View):
    template_name = "pups_to_stock_cage.html"

    def dispatch(self, request, box_no, *args, **kwargs):
        try:
            self.box_no = box_no
            self.cage = BreedingCage.objects.get(box_no=self.box_no)
            self.MouseFormSet = formset_factory(BatchFromBreedingCageForm, extra=0)
        except BreedingCage.DoesNotExist:
            raise Http404("Breeding cage does not exist")
        return super().dispatch(request, *args, **kwargs)

    def get_initial_data(self):
        initial_data = []
        for sex, count in [("M", self.cage.male_pups), ("F", self.cage.female_pups)]:
            initial_data += [
                {
                    "sex": sex,
                    "strain": self.cage.mother.strain,
                    "mother": self.cage.mother,
                    "father": self.cage.father,
                    "dob": self.cage.date_born,
                }
                for _ in range(count)
            ]
        return initial_data

    def get(self, request):
        initial_data = self.get_initial_data()
        formset = self.MouseFormSet(initial=initial_data, prefix="mouse")
        return render(request, self.template_name, {"formset": formset})

    def post(self, request):
        formset = self.MouseFormSet(request.POST, prefix="mouse")
        if formset.is_valid():
            for form in formset:
                mouse_instance = form.save(commit=False)
                mouse_instance.strain = self.cage.mother.strain
                mouse_instance.mother = self.cage.mother
                mouse_instance.father = self.cage.father
                mouse_instance.dob = self.cage.date_born
                mouse_instance.save()
            self.cage.transferred_to_stock = True
            self.cage.save()
            return redirect("breeding_cage:list_breeding_cages")
        return render(request, self.template_name, {"formset": formset})


"""
@login_required
def pups_to_stock_cage(request, box_no):
    cage = BreedingCage.objects.get(box_no=box_no)
    MouseFormSet = formset_factory(BatchFromBreedingCageForm, extra=0)

    if request.method == "POST":
        formset = MouseFormSet(request.POST, prefix="mouse")
        if formset.is_valid():
            for form in formset:
                mouse_instance = form.save(commit=False)
                mouse_instance.strain = cage.mother.strain
                mouse_instance.mother = cage.mother
                mouse_instance.father = cage.father
                mouse_instance.dob = cage.date_born
                mouse_instance.save()
            cage.transferred_to_stock = True
            return redirect("breeding_cage:list_breeding_cages")
    else:
        initial_data_males = [
            {
                "sex": "M",
                "strain": cage.mother.strain,
                "mother": cage.mother,
                "father": cage.father,
                "dob": cage.date_born,
            }
            for _ in range(cage.male_pups)
        ]
        initial_data_females = [
            {
                "sex": "F",
                "strain": cage.mother.strain,
                "mother": cage.mother,
                "father": cage.father,
                "dob": cage.date_born,
            }
            for _ in range(cage.female_pups)
        ]
        initial_data = initial_data_males + initial_data_females
        formset = MouseFormSet(initial=initial_data, prefix="mouse")
    return render(request, "pups_to_stock_cage.html", {"formset": formset})
"""
