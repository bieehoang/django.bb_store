from django.shortcuts import render
from django.http import request
from django.shortcuts import redirect
from cart.models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request, product_id):
    current_user = request.user
    product =  Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variations = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except ObjectDoesNotExist:
                    pass
        
        is_exists_cart_item = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_exists_cart_item:
            cart_items = CartItem.objects.filter(
                product = product,
                user = current_user,
            )
            existing_variation_list = [list(item.variations.all()) for item in cart_items]
            id = [item.id for item in cart_items]
            if product_variations in existing_variation_list:
                index = existing_variation_list.index(product_variations)
                cart_item = CartItem.objects.get(id=id[index])
                cart_item.quantity += 1
            else:
                cart_item = CartItem.objects.create(
                    product = product,
                    user=current_user,
                    quantity=1
                )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                user= current_user,
                quantity =1
            )
        if len(product_variations) > 0:
            cart_item.variations.clear()
            for item in product_variations:
                cart_item.variations.add(item)
        cart_item.save()
        return redirect('cart')
    else:
        product_variations = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except ObjectDoesNotExist:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request=request)) # Get cart using the _cart_id
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id =  _cart_id(request)
            )
        cart.save()
        is_exists_cart_item = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_exists_cart_item:
            cart_items = Cart.objects.filter(
                product=product,
                cart=cart
            )
            existing_variation_list = [list(item.variations.all()) for item in cart_items]
            id = [item.id for item in cart_items]
            if product_variations in existing_variation_list:
                index = existing_variation_list.index(product_variations)
                cart_item = CartItem.objects.get(id=id[index])
                cart_item.quantity += 1
            else:
                cart_item = CartItem.objects.create(
                    product = product,
                    cart=cart,
                    quantity =1
                )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity = 1
            )
        if len(product_variations) > 0:
            cart_item.variations.clear()
            for item in product_variations:
                cart_item.variations.add(item)
        cart_item.save()
        return redirect('cart')
def cart(request, total=0, quantity=0, cart_item=None):
    try: 
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = total * 2/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax if "tax" in locals() else "",
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context=context)