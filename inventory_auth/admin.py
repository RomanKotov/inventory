from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAdminModelProxy, LogEntryModelProxy


@admin.register(UserAdminModelProxy)
class CustomUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LogEntryModelProxy)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "user_url",
        "action_flag",
        "content_type",
        "object_url",
        "change_message",
        "object_repr",
        "action_time",
    )
    list_filter = ('user', 'action_flag', 'content_type')
    list_display_links = None
    search_fields = ('object_repr', 'object_id', 'change_message')
    date_hierarchy = 'action_time'
    list_select_related = ("user", "content_type")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
