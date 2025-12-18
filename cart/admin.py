from django.contrib import admin
from .models import Cart, CartItems, Coupon, Payment


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'discount_price', 'minimum_amount', 'is_expired', 'create_at']
    list_filter = ['is_expired', 'create_at']
    search_fields = ['coupon_code']
    readonly_fields = ['uid', 'create_at', 'updated_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'coupon', 'create_at']
    list_filter = ['is_paid', 'create_at']


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'size_variant', 'color_variant', 'quantity']
    list_filter = ['create_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['cart', 'razorpay_order_id', 'razorpay_payment_id', 'amount', 'status', 'create_at']
    list_filter = ['status', 'create_at']
    search_fields = ['razorpay_order_id', 'razorpay_payment_id']
    readonly_fields = ['uid', 'create_at', 'updated_at']
