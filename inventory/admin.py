from django.contrib import admin
from . import models as m


@admin.register(m.InventoryOwner)
class InventoryOwnerAdmin(admin.ModelAdmin):
    fields = ('fullname', 'status')
    list_display = ('fullname', 'is_active')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(m.InventoryGroup)
class InventoryGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_active')
    fields = ('name', 'owner', 'status')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(m.InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    fields = ('name', 'inventory_number', 'serial_number', 'quantity',
              'location', 'group', 'photo', 'tags', 'status')
    list_display = ('name', 'inventory_number',
                    'serial_number', 'quantity', 'is_active')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(m.Location)
class LocationAdmin(admin.ModelAdmin):
    fields = ('name', 'status')
    list_display = ('name', 'is_active')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(m.LocationHistory)
class LocationHistoryAdmin(admin.ModelAdmin):
    list_display = ('location__name', 'inventory_item', 'created_at',
                    'is_active')
    fields = (
        'location',
        'inventory_item',
        'author',
        'created_at',
        'status'
    )
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(m.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'preview', 'last_used')
    fields = ('image', 'large_preview', 'status')
    readonly_fields = ('large_preview',)
    date_hierarchy = 'last_used'
    ordering = ('-last_used',)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(m.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('type', 'name', 'status')
    list_display = ('name', 'type', 'is_active')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(m.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'entity', 'object_url', 'author',
                    'created_at', 'changed_at', 'is_active')
    fields = ('text', 'entity', 'object_id', 'author',
              'created_at', 'changed_at', 'status')
    readonly_fields = ('created_at', 'changed_at')

    def has_delete_permission(self, request, obj=None):
        return False
