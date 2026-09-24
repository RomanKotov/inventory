from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from .models import InventoryOwner, InventoryGroup, InventoryItem, Tag


def index(request):
    owners = InventoryOwner.active.all()
    return render(request, "inventory/home.html", {
        "owners": owners
    })


def owner(request, owner_id):
    owner = get_object_or_404(InventoryOwner.active, pk=owner_id)
    groups = (
        InventoryGroup.active.filter(owner_id=owner_id)
        .prefetch_related(
            Prefetch(
                "inventoryitem_set",
                queryset=InventoryItem.active.all(),
            ),
            Prefetch(
                "inventoryitem_set__tags",
                queryset=Tag.active.all()
            )
        )
    )
    return render(
        request,
        "inventory/owner.html",
        {"owner": owner, 'groups': groups}
    )
