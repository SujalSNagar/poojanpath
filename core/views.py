from django.shortcuts import render
from products.models import Product, Category


def home(request):
    
    featured_products = Product.objects.filter(
        is_featured=True,
        is_available=True
    )[:8]
    
    temple_essentials = Product.objects.filter(
        category__slug='temple-essentials',
        is_available=True
        )[:4]

    pooja_samagri = Product.objects.filter(
        category__slug='pooja-samagri',
        is_available=True
    )[:4]

    divine_fragrance_products = Product.objects.filter(
        category__slug__in=['agarbatti', 'dhoop'],
        is_available=True
    )

    featured_categories = Category.objects.filter(
        is_featured=True
    )

    context = {
        'featured_products': featured_products,
        'featured_categories': featured_categories,
        'temple_essentials': temple_essentials,
        'divine_fragrance_products': divine_fragrance_products,
        'pooja_samagri': pooja_samagri,
    }

    return render(
        request,
        'core/home.html',
        context
    )

def about_page(request):

    return render(
        request,
        'core/about.html'
    )