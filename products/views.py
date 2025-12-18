from django.shortcuts import render
from django.db import models
from .models import Product, ColorVariant


def get_product(request, slug):
    try:
        product = Product.objects.get(slug = slug)
        context = {'product' : product}
        
        # Calculate base price
        base_price = product.price
        updated_price = base_price
        
        # Handle size selection
        if request.GET.get('size'):
            size = request.GET.get('size')
            updated_price = product.get_product_price_by_size(size)
            context['selected_size'] = size
        
        # Handle color selection
        selected_color = None
        if request.GET.get('color'):
            color_name = request.GET.get('color')
            try:
                selected_color = ColorVariant.objects.get(color_name=color_name)
                # If size is already selected, add color price to the size-adjusted price
                if request.GET.get('size'):
                    updated_price = updated_price + selected_color.price
                else:
                    updated_price = product.get_product_price_by_color(color_name)
                context['selected_color'] = color_name
            except ColorVariant.DoesNotExist:
                pass
        
        # Filter images based on selected color
        # Check if color_variant field exists in ProductImage model (for migration compatibility)
        try:
            if selected_color:
                # Get images for the selected color, or fallback to images without color variant
                images = product.product_images.filter(color_variant=selected_color)
                if not images.exists():
                    # If no color-specific images, show general images (without color variant)
                    images = product.product_images.filter(color_variant__isnull=True)
                    if not images.exists():
                        # If still no images, show all images as fallback
                        images = product.product_images.all()
                context['product_images'] = images
            else:
                # Show images without color variant, or all images if none exist
                images = product.product_images.filter(color_variant__isnull=True)
                if not images.exists():
                    images = product.product_images.all()
                context['product_images'] = images
        except (models.FieldDoesNotExist, Exception) as e:
            # If color_variant field doesn't exist yet (migration not run), show all images
            context['product_images'] = product.product_images.all()
        
        if updated_price != base_price:
            context['updated_price'] = updated_price
            
        return render(request, 'product/product.html', context= context )
        
    except Product.DoesNotExist:
        from django.http import Http404
        raise Http404("Product not found")
    except Exception as e:
        print(e)
        # Return a basic response even on error
        return render(request, 'product/product.html', {'product': None, 'error': str(e)})