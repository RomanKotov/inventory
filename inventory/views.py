from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
import inventory.models as m


def index(request):
    owners = m.InventoryOwner.active.all()
    return render(request, "inventory/home.html", {
        "owners": owners
    })


def owner_page(request, owner_id):
    owner = get_object_or_404(m.InventoryOwner.active, pk=owner_id)
    groups = (
        m.InventoryGroup.active.filter(owner_id=owner_id)
        .prefetch_related(
            Prefetch(
                "inventoryitem_set",
                queryset=m.InventoryItem.active.all(),
            ),
            Prefetch(
                "inventoryitem_set__tags",
                queryset=m.Tag.active.all()
            )
        )
    )
    return render(
        request,
        "inventory/owner.html",
        {"owner": owner, 'groups': groups}
    )


def item_page(request, owner_id, group_id, item_id):
    item = get_object_or_404(
        m.InventoryItem.active.all(),
        id=item_id,
        group_id=group_id,
        group__status=m.Status.ACTIVE,
        group__owner_id=owner_id,
        group__owner__status=m.Status.ACTIVE
    )
    tags = m.Tag.active.filter(inventoryitem=item)
    locations = (
        m.LocationHistory.active
        .filter(inventory_item_id=item_id)
        .order_by('-created_at')
        .prefetch_related('location')
    )
    comments = (
        m.Comment.active
        .filter(inventory_item=item)
        .order_by('created_at')
        .prefetch_related('author')
    )
    return render(
        request,
        "inventory/item.html",
        {
            "item": item,
            "tags": tags,
            "locations": locations,
            "comments": comments
        }
    )
