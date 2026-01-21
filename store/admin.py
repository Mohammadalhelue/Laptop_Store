from django.contrib import admin
from .models import Accessory, SearchHistory, Order, OrderItem


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock')
    search_fields = ('name', 'description', 'category', 'price', 'stock')
    list_filter = ['created_at', 'updated_at']
    list_editable = ['price', 'category']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'created_at')
    search_fields = ('query',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'created_at')
    search_fields = ('first_name', 'last_name', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'quantity', 'accessory', 'price')
    search_fields = ('order', 'quantity', 'accessory', 'price')
