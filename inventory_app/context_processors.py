from django.urls import reverse
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def inventory_settings(request: HttpRequest):
    raw_links = (
        (reverse("home"), _("Home")),
    )
    navbar_links = [
        {
            "href": url,
            "name": text,
            "active": url == request.path
        } for url, text in raw_links
    ]
    return {'navbar_links':  navbar_links}
