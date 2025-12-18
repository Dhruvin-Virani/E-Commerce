from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from products.models import Product, SizeVariant, ColorVariant


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="carts")
    is_paid = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.user.username if self.user else 'Anonymous'} - {self.uid}"
    
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        total = 0
        for cart_item in cart_items:
            total += cart_item.get_product_price()
        return total


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
