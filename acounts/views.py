from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from cart.views import _cart_id
from .forms import RegistrationForm
# from account.models import Account
def register(request):
    if request.method == "GET":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            # user = Account.objects.create_user(
            #     f
            # )

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
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                return redirect('dashboard')
        
        else:
            messages.error(request=request, message="Login Failed")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request, 'accounts/login.html', context = context)

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="Logged out!")
    return redirect('login')