from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import redirect, render

from breeding_cage.models import BreedingCage
from stock_cage.forms import BatchFromBreedingCageForm


@login_required
def transfer_to_stock_cage(request, box_no):
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
    return render(request, "transfer_to_stock_cage.html", {"formset": formset})
