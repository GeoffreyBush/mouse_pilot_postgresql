from django.urls import path

from wean_pups.views import PupsToStockCageView

app_name = "wean_pups"

urlpatterns = [
    path(
        "pups_to_stock_cage/<str:box_no>",
        PupsToStockCageView.as_view(),
        name="pups_to_stock_cage",
    ),
]
