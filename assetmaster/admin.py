from django.contrib import admin
from .models import AssetType,Item,AssetImage
# Register your models here.

class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ['asset_type','asset_description','created_at','updated_at']

admin.site.register(AssetType,AssetTypeAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name','asset_type','is_active','created_at','updated_at']

admin.site.register(Item,ItemAdmin)

class AssetImageAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'item_image']

admin.site.register(AssetImage,AssetImageAdmin)