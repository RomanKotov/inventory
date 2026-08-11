from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

STATUS_SIZE = 10


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


class Photo(models.Model):
    image = models.ImageField(
        _("image"),
        upload_to="images/"
    )
    last_used = models.DateTimeField(
        _("last used"),
        auto_now_add=True
    )
    status = models.CharField(
        _("status"),
        max_length=STATUS_SIZE,
        choices=Status,
        default=Status.ACTIVE
    )


class Tag(models.Model):
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
    status = models.CharField(
        _("status"),
        max_length=STATUS_SIZE,
        choices=Status,
        default=Status.ACTIVE
    )


class Location(models.Model):
    name = models.CharField(
        _("name"),
        max_length=255,
    )
    status = models.CharField(
        _("status"),
        max_length=STATUS_SIZE,
        choices=Status,
        default=Status.ACTIVE
    )


class LocationHistory(models.Model):
    location = models.ForeignKey(
        Location,
        verbose_name=_("location"),
        on_delete=models.PROTECT,
    )
    inventory_item = models.ForeignKey(
        'InventoryItem',
        verbose_name=_("inventory item"),
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(
        _("created_at"),
        auto_now_add=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        _("status"),
        max_length=STATUS_SIZE,
        choices=Status,
        default=Status.ACTIVE
    )


class InventoryOwner(models.Model):
    fullname = models.CharField(
        _("fullname"),
        max_length=150,
        help_text=_("Name of inventory owner")
    )
    status = models.CharField(
        _("status"),
        max_length=STATUS_SIZE,
        choices=Status,
        default=Status.ACTIVE
    )


class InventoryGroup(models.Model):
    name = models.CharField(
        _("name"),
        max_length=255,
    )
    owner = models.ForeignKey(
        InventoryOwner,
        verbose_name=_("owner"),
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        _("status"),
        max_length=STATUS_SIZE,
        choices=Status,
        default=Status.ACTIVE
    )


class InventoryItem(models.Model):
    group = models.ForeignKey(
        InventoryGroup,
        verbose_name=_("group"),
        on_delete=models.PROTECT,
    )
    photo = models.ForeignKey(
        Photo,
        verbose_name=_("photo"),
        on_delete=models.PROTECT,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tags"),
    )
    location = models.ForeignKey(
        Location,
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
    status = models.CharField(
        _("status"),
        max_length=STATUS_SIZE,
        choices=Status,
        default=Status.ACTIVE
    )


class Comment(models.Model):
    name = models.TextField(
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
    status = models.CharField(
        _("status"),
        max_length=STATUS_SIZE,
        choices=Status,
        default=Status.ACTIVE
    )
