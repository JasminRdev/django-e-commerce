from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q


from django.http import HttpResponse
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        #products 8
        #paginator shows 6 each site
        products = Product.objects.all().filter(is_available=True).order_by('id')
        
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    

    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        # syntax "__slug" gives access to slug of model 
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)

        # cart__cart_id is accessing the cart_id through CartItem in Cart with foreign key / models
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    
    return render(request, 'store/product_detail.html', context)


def search(request):
    #checks if keyword exists in url that is in navbar html searchs input name attribute
        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            #find by filter through descriptions model
            if keyword:
                products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        context = {'products': products,}
        return render(request, 'store/store.html', context)