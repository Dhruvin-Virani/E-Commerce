from django.contrib import admin
from .models import Cart, CartItems


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'create_at']
    list_filter = ['is_paid', 'create_at']


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'size_variant', 'color_variant', 'quantity']
    list_filter = ['create_at']
