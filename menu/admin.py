from django.contrib import admin
from .models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'is_available', 'created_at')
	list_filter = ('is_available', 'category')
	search_fields = ('name', 'description', 'category')
