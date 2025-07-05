from django.contrib import admin
from .models import Product, OrderDetail

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'total_sales_amount', 'total_orders', 'current')
    fields = ('name', 'description', 'price', 'file', 'preview_image', 'mockup_image', 'total_sales_amount', 'total_orders', 'current')

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('customer_email', 'product', 'amount', 'has_paid', 'created_on')
    fields = ('customer_email', 'product', 'amount', 'stripe_payment_intent', 'has_paid',)
