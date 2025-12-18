from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def get_product(request, slug):
    """Display a single product. If `size` is provided in GET, compute price for that size."""
    product = get_object_or_404(Product, slug=slug)
    context = { 'product': product }

    size = request.GET.get('size')
    if size:
        try:
            context['price'] = product.get_product_price_by_size(size)
        except Exception as e:
            # If size not found or other error, just log and continue
            print(e)

    return render(request, 'product/product.html', context=context)


def category_view(request, slug):
    """List products under a category identified by slug."""
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'products/category.html', { 'category': category, 'products': products })