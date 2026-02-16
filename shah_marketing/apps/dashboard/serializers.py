from rest_framework import serializers


class SalesAnalyticsSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=14, decimal_places=2)
    delivered_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
