from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect


class PermissionCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        can_skip_logged_in_check = any(
            request.path.startswith(r)
            for r in settings.ROUTES_SKIP_PERMISSION_CHECKS
        )
        if can_skip_logged_in_check:
            return self.get_response(request)

        if request.user.is_authenticated:
            return self.get_response(request)

        if request.method == "GET":
            return redirect("login")

        raise PermissionDenied
