from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class UserAdminModelProxy(User):
    class Meta:
        proxy = True
        app_label = "auth"
        verbose_name = _("user")
        verbose_name_plural = _("users")
