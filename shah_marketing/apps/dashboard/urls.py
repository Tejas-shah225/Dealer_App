from django.urls import path

from .views import SalesAnalyticsView

urlpatterns = [
    path('sales-analytics/', SalesAnalyticsView.as_view(), name='sales-analytics'),
]
