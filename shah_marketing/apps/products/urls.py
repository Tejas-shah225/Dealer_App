from django.urls import path

from .views import (
    AdminProductListCreateView,
    AdminProductRetrieveUpdateDestroyView,
    CategoryListView,
    ProductDetailView,
    ProductListView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('admin/products/', AdminProductListCreateView.as_view(), name='admin-product-list-create'),
    path('admin/products/<int:pk>/', AdminProductRetrieveUpdateDestroyView.as_view(), name='admin-product-detail'),
]
