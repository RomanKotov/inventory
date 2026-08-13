from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html


def generic_admin_object_url(content_type, object_id):
    try:
        url = reverse(
            f'admin:{content_type.app_label}_{content_type.model}_change',
            args=[object_id]
        )
        return format_html('<a href="{}">{}</a>', url, object_id)
    except NoReverseMatch:
        return object_id
