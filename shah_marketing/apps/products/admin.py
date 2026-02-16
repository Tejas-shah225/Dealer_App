from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'stock_quantity', 'stock_warning', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('created_at',)

    def stock_warning(self, obj):
        if obj.stock_quantity < 10:
            return format_html('<span style="color: #b91c1c; font-weight: bold;">Low Stock</span>')
        return format_html('<span style="color: #15803d;">Healthy</span>')

    stock_warning.short_description = 'Stock status'
