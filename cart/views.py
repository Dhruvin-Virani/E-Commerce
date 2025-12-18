from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItems
from products.models import Product, SizeVariant, ColorVariant


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    else:
        # For anonymous users, use session-based cart
        if not request.session.session_key:
            request.session.create()
        
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(uid=cart_id, user=None, is_paid=False)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=None, is_paid=False)
                request.session['cart_id'] = str(cart.uid)
        else:
            cart = Cart.objects.create(user=None, is_paid=False)
            request.session['cart_id'] = str(cart.uid)
    
    return cart


def get_cart_count(request):
    """Get cart count for AJAX requests"""
    cart = get_cart(request)
    count = cart.cart_items.count()
    return JsonResponse({'count': count})


@require_POST
def add_to_cart(request):
    try:
        product_slug = request.POST.get('product_slug')
        size = request.POST.get('size', '')
        color = request.POST.get('color', '')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, slug=product_slug)
        cart = get_cart(request)
        
        # Get size and color variants if provided
        size_variant = None
        color_variant = None
        
        if size:
            try:
                size_variant = SizeVariant.objects.get(size=size)
            except SizeVariant.DoesNotExist:
                pass
        
        if color:
            try:
                color_variant = ColorVariant.objects.get(color_name=color)
            except ColorVariant.DoesNotExist:
                pass
        
        # Check if cart item with same product, size, and color already exists
        cart_item, created = CartItems.objects.get_or_create(
            cart=cart,
            product=product,
            size_variant=size_variant,
            color_variant=color_variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart successfully',
                'cart_count': cart.cart_items.count()
            })
        
        messages.success(request, 'Product added to cart successfully')
        return redirect('cart')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        messages.error(request, f'Error: {str(e)}')
        return redirect('get_product', slug=product_slug)


def cart_view(request):
    cart = get_cart(request)
    cart_items = cart.cart_items.all()
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def remove_from_cart(request, cart_item_uid):
    
    try:
        cart_item = get_object_or_404(CartItems, uid=cart_item_uid)
        cart = cart_item.cart
        
        # Check if user owns this cart
        if request.user.is_authenticated:
            if cart.user != request.user:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
                messages.error(request, 'You do not have permission to remove this item')
                return redirect('cart')
        else:
            session_cart_id = request.session.get('cart_id')
            if str(cart.uid) != session_cart_id:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
                messages.error(request, 'You do not have permission to remove this item')
                return redirect('cart')
        
        cart_item.delete()
        
        # Refresh cart from database to get updated total
        cart.refresh_from_db()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cart_total': cart.get_cart_total()
            })
        
        messages.success(request, 'Item removed from cart')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('cart')


@require_POST
def update_cart_item(request, cart_item_uid):
    try:
        cart_item = get_object_or_404(CartItems, uid=cart_item_uid)
        cart = cart_item.cart
        
        # Check if user owns this cart
        if request.user.is_authenticated:
            if cart.user != request.user:
                return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
        else:
            session_cart_id = request.session.get('cart_id')
            if str(cart.uid) != session_cart_id:
                return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
        
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            cart_item.delete()
            item_total = 0
        else:
            cart_item.quantity = quantity
            cart_item.save()
            item_total = cart_item.get_product_price()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response_data = {
                'success': True,
                'message': 'Cart updated successfully',
                'cart_total': cart.get_cart_total(),
            }
            if quantity > 0:
                response_data['item_total'] = item_total
            else:
                response_data['item_deleted'] = True
            return JsonResponse(response_data)
        
        messages.success(request, 'Cart updated successfully')
        return redirect('cart')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        messages.error(request, f'Error: {str(e)}')
        return redirect('cart')
