from django.urls import path

from breeding_cage import views

app_name = "breeding_cage"

urlpatterns = [
    path(
        "list_breeding_cages",
        views.list_breeding_cages,
        name="list_breeding_cages",
    ),
    path("add_breeding_cage", views.add_breeding_cage, name="add_breeding_cage"),
    path(
        "view_breeding_cage/<str:box_no>",
        views.view_breeding_cage,
        name="view_breeding_cage",
    ),
    path(
        "edit_breeding_cage/<str:box_no>",
        views.edit_breeding_cage,
        name="edit_breeding_cage",
    ),
    path(
        "transfer_to_stock_cage/<str:box_no>",
        views.transfer_to_stock_cage,
        name="transfer_to_stock_cage",
    ),
]
