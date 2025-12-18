from .views import get_cart
from products.models import Category


def cart_count(request):
    """Context processor to add cart count to all templates"""
    try:
        cart = get_cart(request)
        cart_count = cart.cart_items.count()
    except:
        cart_count = 0
    
    return {'cart_count': cart_count}


def categories(request):
    """Context processor to add categories to all templates"""
    try:
        categories = Category.objects.all()[:10]
    except:
        categories = []
    
    return {'categories': categories}

