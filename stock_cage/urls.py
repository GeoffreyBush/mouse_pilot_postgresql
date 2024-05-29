from django.urls import path

from stock_cage import views

app_name = "stock_cage"

urlpatterns = [
    path(
        "transfer_to_stock_cage/<str:box_no>",
        views.transfer_to_stock_cage,
        name="transfer_to_stock_cage",
    )
]
