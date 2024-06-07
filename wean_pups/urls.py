from django.urls import path

from wean_pups import views

app_name = "wean_pups"

urlpatterns = [
    path(
        "pups_to_stock_cage/<str:box_no>",
        views.pups_to_stock_cage,
        name="pups_to_stock_cage",
    ),
]
