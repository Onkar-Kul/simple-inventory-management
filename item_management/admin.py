from django.contrib import admin

from item_management.models import Item


# Register your models here.
@admin.register(Item)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description', 'quantity', 'price', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'description')
