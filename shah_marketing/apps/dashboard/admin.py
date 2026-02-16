from django.contrib import admin
from django.db.models import Sum

from apps.orders.models import Order


class DashboardAdminSite(admin.AdminSite):
    site_header = 'Shah Marketing Administration'
    site_title = 'Shah Marketing Admin'
    index_title = 'Operations Dashboard'

    def each_context(self, request):
        context = super().each_context(request)
        sales = Order.objects.aggregate(total_sales=Sum('total_amount'))
        context['total_sales'] = sales['total_sales'] or 0
        context['total_orders'] = Order.objects.count()
        return context


dashboard_admin_site = DashboardAdminSite(name='dashboard_admin')
