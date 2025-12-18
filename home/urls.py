from django.urls import path
from home.views import index, search

urlpatterns = [
    path('', index, name="index"),
    path('search/', search, name="search"),
]
