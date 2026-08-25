from django.contrib import messages
from django.shortcuts import render


def index(request):
    messages.success(request, "Hello, world!")

    return render(request, "inventory/home.html", {})
