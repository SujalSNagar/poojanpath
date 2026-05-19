from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'

urlpatterns = [

    path('search/', views.product_search, name='search'),
    path('all-products/',views.all_products,name='all_products'),
    path('category/<slug:slug>/',views.category_products,name='category_products'),
    path('<slug:slug>/', views.product_detail, name='detail'),

    path(
    'collection/<slug:section_slug>/',
    views.collection_page,
    name='collection_page'
),

]