from django.shortcuts import render
from products.models import Product, Category


# Create your views here.
def index(request):
    products = Product.objects.all()[:12]  # Show 12 products on homepage
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'home/index.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            product_name__icontains=query
        ) | Product.objects.filter(
            product_description__icontains=query
        )
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'home/search.html', context)