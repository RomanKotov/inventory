from django.db.models import Prefetch, Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
import inventory.models as m


def index(request: HttpRequest):
    owners = m.InventoryOwner.active.all()
    return render(request, "inventory/home.html", {
        "owners": owners
    })


def owner_page(request: HttpRequest, owner_id: int):
    owner = get_object_or_404(m.InventoryOwner.active, pk=owner_id)
    search = request.GET.get("search", "")
    related_items = (
        m.InventoryItem.active.filter(
            Q(name__contains=search)
            | Q(serial_number__contains=search)
            | Q(inventory_number__contains=search)
            | Q(quantity__contains=search)
        )
    )
    groups = (
        m.InventoryGroup.active.filter(owner_id=owner_id)
        .prefetch_related(
            Prefetch("inventoryitem_set", queryset=related_items),
            Prefetch(
                "inventoryitem_set__tags",
                queryset=m.Tag.active.all()
            )
        )
    )
    return render(
        request,
        "inventory/owner.html",
        {
            "owner": owner,
            "groups": groups,
            "search": search
        }
    )


def item_page(
        request: HttpRequest, owner_id: int, group_id: int, item_id: int
):
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
