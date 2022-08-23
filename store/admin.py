from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin_price', 'price', 'stock',
                    'category', 'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
