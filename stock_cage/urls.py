from django.urls import path

from stock_cage import views

app_name = "stock_cage"

urlpatterns = [
    path("list_stock_cages/", views.list_stock_cages, name="list_stock_cages"),
    path("add_stock_cage/", views.add_stock_cage, name="add_stock_cage"),
]
