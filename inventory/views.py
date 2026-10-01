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
