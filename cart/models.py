from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from products.models import Product, SizeVariant, ColorVariant


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=50, unique=True)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=0)
    minimum_amount = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.coupon_code} - ₹{self.discount_price} off"
    
    def is_valid(self, cart_total):
        """Check if coupon is valid for the given cart total"""
        if self.is_expired:
            return False
        if cart_total < self.minimum_amount:
            return False
        return True


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="carts")
    is_paid = models.BooleanField(default=False)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.user.username if self.user else 'Anonymous'} - {self.uid}"
    
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        total = 0
        for cart_item in cart_items:
            total += cart_item.get_product_price()
        return total
    
    def get_cart_total_after_discount(self):
        """Get cart total after applying coupon discount"""
        total = self.get_cart_total()
        if self.coupon and self.coupon.is_valid(total):
            discount = self.coupon.discount_price
            return max(0, total - discount)  # Ensure total doesn't go negative
        return total
    
    def get_discount_amount(self):
        """Get the discount amount if coupon is applied"""
        total = self.get_cart_total()
        if self.coupon and self.coupon.is_valid(total):
            return self.coupon.discount_price
        return 0


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return f"{self.product.product_name if self.product else 'Deleted Product'} - {self.quantity}"
    
    def get_product_price(self):
        if not self.product:
            return 0
        
        price = self.product.price
        
        if self.size_variant:
            price += self.size_variant.price
        
        if self.color_variant:
            price += self.color_variant.price
        
        return price * self.quantity
