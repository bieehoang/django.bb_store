from django.urls import path
from . import views

urlpartterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>', views.product_detail, name='product_detail')
]
