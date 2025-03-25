from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "HEAD"])
def health_check(request):
    """Handle both GET and HEAD requests"""
    response = HttpResponse("OK", content_type="text/plain", status=200)
    response.headers["Cache-Control"] = "no-store"
    return response