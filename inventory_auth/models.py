from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .url_helpers import generic_admin_object_url


class User(AbstractUser):
    pass


class UserAdminModelProxy(User):
    class Meta:
        proxy = True
        app_label = "auth"
        verbose_name = _("user")
        verbose_name_plural = _("users")


class LogEntryModelProxy(LogEntry):
    class Meta:
        proxy = True
        app_label = "auth"
        verbose_name = _("audit log")
        verbose_name_plural = _("audit logs")

    @admin.display(description=_("user"))
    def user_url(self):
        return format_html(
            '<a href="{}">{}</a>',
            reverse(
                'admin:auth_useradminmodelproxy_change',
                args=[self.user_id]
            ),
            self.user
        )

    @admin.display(description="object url")
    def object_url(self):
        return generic_admin_object_url(
            self.content_type,
            self.object_id
        )
