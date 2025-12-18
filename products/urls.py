from django.urls import path
from products.views import get_product, category_view

urlpatterns = [
    path('category/<slug>/', category_view, name="category_view"),
    path('<slug>/', get_product, name="get_product"),
]
