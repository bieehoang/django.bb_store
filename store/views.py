from django.shortcuts import render
from .models import Product
from category.models import Category
from cart.models import Cart, CartItem
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q 
from cart.views import _cart_id

def store(request, category_slug=None):
    """
    Create view for tab products
    """
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 3)
    paged_products = paginator.get_page(page)
    product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context=context)

def product_detail(request, category_slug, product_slug = None):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        in_cart = CartItem.objects.filter(
            cart=cart,
            product=single_product
        ).exists()
    except Exception as e:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )

    # try:
    #     orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    # except Exception:
    #     orderproduct = None

    # reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        'single_product': single_product, #type: ignore
        'in_cart': in_cart if 'in_cart' in locals() else False, #type:ignore
        # 'orderproduct': orderproduct,
        # 'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context=context)

def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        products = Product.objects.order_by('-created_date').filter(Q(product_name=q) | Q(description=q))
        product_count = products.count()
    context = {
        'q': q, #type: ignore
        'products': products, #type: ignore
        'product_count': product_count,#type: ignore
    }
    return render(request, 'store/store.html', context=context)