from django.http import HttpResponse
from django.views.decorators.http import require_GET

@require_GET
def health_check(request):
    """Bypass all middleware checks"""
    return HttpResponse(
        "OK",
        content_type="text/plain",
        status=200,
        headers={"Cache-Control": "no-store"}
    )