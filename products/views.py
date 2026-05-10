from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Product,Category

from django.db.models import Q
# Create your views here.

def product_detail(request, slug):
        product = get_object_or_404(Product,slug=slug)
        
        return render(request, 'products/product_detail.html' , {'product': product})

def all_products(request):

    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(
        request,
        'products/all_products.html',
        context
    )

def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    products = Product.objects.filter(
        category=category
    )

    context = {
        'category': category,
        'products': products,
    }

    return render(
        request,
        'products/category_products.html',
        context
    )

def product_search(request):

    query = request.GET.get('q')

    products = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
        )

    context = {
        'query': query,
        'products': products,
    }

    return render(request, 'products/search.html', context)