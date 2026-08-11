from django.contrib import admin
from . import models as m

admin.site.register(m.InventoryOwner)
admin.site.register(m.InventoryGroup)
admin.site.register(m.InventoryItem)
admin.site.register(m.Location)
admin.site.register(m.LocationHistory)
admin.site.register(m.Photo)
admin.site.register(m.Tag)
admin.site.register(m.Comment)
