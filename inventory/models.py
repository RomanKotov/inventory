from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from inventory_auth.url_helpers import generic_admin_object_url


class TagType(models.TextChoices):
    PRIMARY = "primary", _("Primary")
    SECONDARY = "secondary", _("Secondary")
    SUCCESS = "success", _("Success")
    DANGER = "danger", _("Danger")
    WARNING = "warning", _("Warning")
    INFO = "info", _("Info")
    LIGHT = "light", _("Light")
    DARK = "dark", _("Dark")


class Status(models.TextChoices):
    ACTIVE = "ACTIVE", _("ACTIVE")
    ARCHIVE = "ARCHIVE", _("ARCHIVE")


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Status.ACTIVE)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = models.Manager()
    active = ActiveManager()
    status = models.CharField(
        _("status"),
        max_length=10,
        choices=Status,
        default=Status.ACTIVE
    )

    @admin.display(description=_("active"), boolean=True)
    def is_active(self):
        return self.status == Status.ACTIVE


class Photo(BaseModel):
    image = models.ImageField(
        _("image"),
        upload_to="images/"
    )
    last_used = models.DateTimeField(
        _("last used"),
        auto_now_add=True
    )

    @admin.display(description=_("preview"))
    def preview(self):
        return format_html(
            ('<img src="{}" style="max-width: 5em; '
             'max-height: 5em; border: 0.1px solid black;">'),
            self.image.url
        )

    @admin.display(description=_("preview"))
    def large_preview(self):
        return format_html(
            '<img src="{}" style="border: 0.1px solid black;>',
            self.image.url
        )


class Tag(BaseModel):
    name = models.CharField(
        _("name"),
        max_length=20,
    )
    type = models.CharField(
        _("type"),
        max_length=10,
        choices=TagType,
        default=TagType.INFO
    )

    def __str__(self):
        return self.name


class Location(BaseModel):
    name = models.CharField(
        _("name"),
        max_length=255,
    )

    def __str__(self):
        return self.name


class InventoryOwner(BaseModel):
    fullname = models.CharField(
        _("fullname"),
        max_length=150,
        help_text=_("Name of inventory owner")
    )

    def __str__(self):
        return self.fullname


class InventoryGroup(BaseModel):
    name = models.CharField(
        _("name"),
        max_length=255,
    )
    owner = models.ForeignKey(
        InventoryOwner,
        verbose_name=_("owner"),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name


class InventoryItem(BaseModel):
    group = models.ForeignKey(
        InventoryGroup,
        verbose_name=_("group"),
        on_delete=models.PROTECT,
    )
    photo = models.ForeignKey(
        Photo,
        verbose_name=_("photo"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name=_("tags"),
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        verbose_name=_("location"),
        on_delete=models.PROTECT,
    )
    inventory_number = models.CharField(
        _("inventory number"),
        unique=True,
        null=True,
        blank=True
    )
    serial_number = models.CharField(
        _("serial number"),
        unique=True,
        null=True,
        blank=True
    )
    quantity = models.IntegerField(
        _("quantity"),
        default=1
    )
    name = models.CharField(
        _("name"),
        max_length=255,
    )

    def __str__(self):
        return self.name


class LocationHistory(BaseModel):
    class Meta:
        verbose_name = _("Location history")
        verbose_name_plural = _("Location histories")

    location = models.ForeignKey(
        Location,
        verbose_name=_("location"),
        on_delete=models.PROTECT,
    )
    inventory_item = models.ForeignKey(
        InventoryItem,
        verbose_name=_("inventory item"),
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.location.name


class Comment(BaseModel):
    text = models.TextField(
        _("text"),
        max_length=255,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True
    )
    changed_at = models.DateTimeField(
        _("changed at"),
        auto_now=True
    )
    entity = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("entity"),
    )
    object_id = models.PositiveIntegerField(
        _("object id"),
    )
    content_object = GenericForeignKey("entity", "object_id")

    def __str__(self):
        max_size = 15
        if len(self.text) < max_size:
            return self.text

        return self.text[:max_size] + "..."

    @admin.display(description=_("object url"))
    def object_url(self):
        return generic_admin_object_url(self.entity, self.object_id)
