from django.shortcuts import render
from products.models import Product, Category


def home(request):
    
    featured_products = Product.objects.filter(
        is_featured=True,
        is_available=True
    )[:8]


    featured_categories = Category.objects.filter(
        is_featured=True
    )

    context = {
        'featured_products': featured_products,
        'featured_categories': featured_categories,
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