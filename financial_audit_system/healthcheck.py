# from django.http import HttpResponse
# from django.views.decorators.http import require_http_methods  # Changed from require_GET
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# @require_http_methods(["GET", "HEAD"])  # Explicitly allow both GET and HEAD
# def health_check(request):
#     """Handle both GET and HEAD requests"""
#     response = HttpResponse("OK", content_type="text/plain", status=200)
#     # HEAD requests shouldn't return a body
#     if request.method == "HEAD":
#         response.content = b""
#     return response

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    """Minimal health check that always passes"""
    return HttpResponse("", status=200, content_type="text/plain")