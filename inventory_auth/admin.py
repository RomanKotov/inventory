from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAdminModelProxy

admin.site.register(UserAdminModelProxy, UserAdmin)
