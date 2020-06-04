from django.urls import path

from products.views import (
    ProductListView, 
    ProductDetailSlugView
    )

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('products/<slug:slug>/', ProductDetailSlugView.as_view()),    
]

