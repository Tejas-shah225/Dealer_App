from django.urls import path

from .views import (
    AdminOrderStatusUpdateView,
    CartAddView,
    CartRemoveView,
    CartView,
    CreateOrderView,
    OrderDetailView,
    OrderListView,
)

urlpatterns = [
    path('cart/add/', CartAddView.as_view(), name='cart-add'),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/remove/<int:pk>/', CartRemoveView.as_view(), name='cart-remove'),
    path('orders/create/', CreateOrderView.as_view(), name='order-create'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('admin/orders/<int:pk>/status/', AdminOrderStatusUpdateView.as_view(), name='admin-order-status-update'),
]
