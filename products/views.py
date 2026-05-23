from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Product,Category

from django.db.models import Q

from datetime import timedelta

from django.utils import timezone


def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    related_products = Product.objects.filter(
        Q(category = product.category)
        |
        Q(subcategory = product.subcategory)
    ).exclude(
        id = product.id
    )

    start_date = (timezone.now().date() + timedelta(days=7))

    end_date = (timezone.now().date() + timedelta(days=10))


    context = {

        'product': product,

        'related_products': related_products,

        'quantity_range': range(1, min(product.stock, 10) + 1),

        'start_date': start_date,

        'end_date': end_date,
    }

    return render(request, 'products/product_detail.html',context)

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

def collection_page(request, section_slug):

    section_map = {

        'divine-fragrance': ['agarbatti', 'dhoop'],

        'temple-essentials': ['diya', 'hand-bell', 'kalash', 'pooja-thali'],

        'brass-collection': ['brass-cup-holder-dhoop', 'brass-oil-container','diya','pooja-thali'],
    }

    slugs = section_map.get(section_slug, [])

    products = Product.objects.filter(
        is_available=True
    ).filter(
        Q(category__slug__in=slugs) |
        Q(subcategory__slug__in=slugs)
    ).distinct()


    context = {
        'products': products,
        'section_slug': section_slug,
    }

    return render(
        request,
        'products/collection_page.html',
        context
    )