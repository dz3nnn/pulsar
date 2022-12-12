from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Product


def products_endpoint(request):
    if request.method == "GET":
        return get_products(request)
    return JsonResponse("GET allowed", status=404)


def product_by_id_endpoint(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return JsonResponse(product.to_dict())


def get_products(request):
    products = Product.objects.all()
    products = make_search(request, products)
    products = make_filter(request, products)
    return JsonResponse([x.to_dict() for x in products], safe=False)


def make_search(request, products):
    q = request.GET.get("q", False)
    if q:
        products = products.filter(Q(name__contains=q) | Q(sku__contains=q))
    return products


def make_filter(request, products):
    status_filter = request.GET.get("status", False)
    if status_filter:
        products = products.filter(status=status_filter.upper())
    return products
