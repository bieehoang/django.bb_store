from django.shortcuts import render
from django.http import request
from django.shortcuts import redirect
from store.models import Product
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    return redirect('cart')