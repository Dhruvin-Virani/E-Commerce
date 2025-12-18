from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Cart, Payment
from .payment_utils import create_razorpay_order, verify_payment_signature, generate_invoice_pdf
from .views import get_cart
from base.emails import send_invoice_email
import uuid


def initiate_payment(request):
    """Initiate payment for cart"""
    try:
        cart = get_cart(request)
        cart_items = cart.cart_items.all()
        
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty')
            return redirect('cart')
        
        # Calculate amount in paise
        total_amount = cart.get_cart_total_after_discount()
        amount_in_paise = int(total_amount * 100)  # Convert to paise
        
        if amount_in_paise <= 0:
            messages.error(request, 'Invalid amount')
            return redirect('cart')
        
        # Create or get payment
        payment, created = Payment.objects.get_or_create(
            cart=cart,
            defaults={
                'amount': amount_in_paise,
                'status': 'Created'
            }
        )
        
        # Create Razorpay order
        receipt_id = f'receipt_{cart.uid}'
        notes = {
            'cart_id': str(cart.uid),
            'user_id': str(cart.user.id) if cart.user else 'anonymous'
        }
        
        razorpay_order = create_razorpay_order(
            amount=amount_in_paise,
            receipt_id=receipt_id,
            notes=notes
        )
        
        # Update payment with order ID
        payment.razorpay_order_id = razorpay_order['id']
        payment.amount = amount_in_paise
        payment.save()
        
        # Prepare context for payment page
        context = {
            'cart': cart,
            'payment': payment,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount_in_paise,
            'amount_in_rupees': total_amount,
            'user_email': cart.user.email if cart.user else '',
            'user_name': cart.user.get_full_name() if cart.user else 'Guest',
            'user_contact': cart.user.profile.phone_number if cart.user and hasattr(cart.user, 'profile') else '',
        }
        
        return render(request, 'cart/payment.html', context)
        
    except Exception as e:
        messages.error(request, f'Error initiating payment: {str(e)}')
        return redirect('cart')


@require_POST
def verify_payment(request):
    """Verify payment after Razorpay callback"""
    try:
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return JsonResponse({'success': False, 'message': 'Missing payment parameters'}, status=400)
        
        # Verify signature
        if not verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
            return JsonResponse({'success': False, 'message': 'Payment verification failed'}, status=400)
        
        # Get payment
        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
        
        # Update payment
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'Success'
        payment.save()
        
        # Mark cart as paid
        cart = payment.cart
        cart.is_paid = True
        cart.save()
        
        # Generate invoice PDF
        try:
            generate_invoice_pdf(payment)
        except Exception as e:
            print(f"Error generating invoice: {str(e)}")
        
        # Send invoice email
        try:
            if cart.user and cart.user.email:
                send_invoice_email(cart.user.email, payment)
        except Exception as e:
            print(f"Error sending invoice email: {str(e)}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Payment successful',
                'payment_id': str(payment.uid)
            })
        else:
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(f'/cart/payment/success/{payment.uid}/')
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def payment_success(request, payment_id):
    """Payment success page"""
    try:
        payment = get_object_or_404(Payment, uid=payment_id)
        amount_in_rupees = payment.amount / 100
        context = {
            'payment': payment,
            'cart': payment.cart,
            'amount_in_rupees': int(amount_in_rupees)
        }
        return render(request, 'cart/payment_success.html', context)
    except Exception as e:
        messages.error(request, 'Payment not found')
        return redirect('cart')

