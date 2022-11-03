from django.shortcuts import render
from django.http import HttpRequest, request
from .models import Product
def store(request):
    products = Product.objects.all().filter(is_available = True)
    context = {
        'links': products,
    }
    return render(request, 'navbar.html', context=context)