from django.contrib import admin
from .models import Accessory, SearchHistory


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock')
    search_fields = ('name', 'description')


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'created_at')
    search_fields = ('query',)
