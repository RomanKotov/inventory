from django.db.models import Prefetch
from django.shortcuts import render
from .models import InventoryOwner, InventoryGroup


def index(request):
    owners = InventoryOwner.active.all().prefetch_related(
        Prefetch(
            "inventorygroup_set",
            queryset=InventoryGroup.active.all()
        )
    )
    return render(request, "inventory/home.html", {
        "owners": owners
    })
