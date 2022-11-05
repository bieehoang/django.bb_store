from django.shortcuts import render
from django.contrib import auth, messages

from cart.models import Cart, CartItem
from cart.views import _cart_id

def login(request):
    if request.mothod == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)
                if cart_items.exists():
                    product_variation = []
                    for cart_item in cart_items:
                        variations = cart_item.variations.all # type: ignore
                        product_variation.append(list(variations))
                    cart_items = CartItem.objects.filter(user=user)
                    existing_variation_list = [list(item.vatiations.all()) for item in cart_items] #type: ignore
                    id = [item.id for item in cart_items]

                    for product in product_variation:
                        if product in existing_variation_list:
                            index = existing_variation_list.index(product)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else: 
                            cart_items = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
            except Exception:
                pass
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login Successfully")

            url = request.META.get("HTTP_REFERER")
            try:
                query = request.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
