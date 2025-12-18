from django.urls import path
from .views import add_to_cart, cart_view, remove_from_cart, update_cart_item, get_cart_count

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('remove/<uuid:cart_item_uid>/', remove_from_cart, name='remove_from_cart'),
    path('update/<uuid:cart_item_uid>/', update_cart_item, name='update_cart_item'),
    path('count/', get_cart_count, name='get_cart_count'),
]

