from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.products_endpoint),
    path("products/<int:product_id>/", views.product_by_id_endpoint),
]
