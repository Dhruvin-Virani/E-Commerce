from django.urls import path
from .views import add_to_cart, cart_view, remove_from_cart, update_cart_item, get_cart_count, apply_coupon, remove_coupon
from .payment_views import initiate_payment, verify_payment, payment_success

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('remove/<uuid:cart_item_uid>/', remove_from_cart, name='remove_from_cart'),
    path('update/<uuid:cart_item_uid>/', update_cart_item, name='update_cart_item'),
    path('count/', get_cart_count, name='get_cart_count'),
    path('coupon/apply/', apply_coupon, name='apply_coupon'),
    path('coupon/remove/', remove_coupon, name='remove_coupon'),
    path('payment/', initiate_payment, name='initiate_payment'),
    path('payment/verify/', verify_payment, name='verify_payment'),
    path('payment/success/<uuid:payment_id>/', payment_success, name='payment_success'),
]

