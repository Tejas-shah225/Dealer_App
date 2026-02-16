from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole
from apps.orders.models import Order


class SalesAnalyticsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        data = Order.objects.aggregate(
            total_orders=Count('id'),
            total_sales=Coalesce(Sum('total_amount'), 0),
            delivered_orders=Count('id', filter=Q(status=Order.Status.DELIVERED)),
            pending_orders=Count('id', filter=Q(status=Order.Status.PENDING)),
        )
        return Response(data)
