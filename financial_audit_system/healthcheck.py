from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
@require_GET
def health_check(request):
    """More robust health check that verifies database connectivity when enabled"""
    if settings.HEALTHCHECK_ENABLED:
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return HttpResponse("OK", content_type="text/plain", status=200)
        except Exception as e:
            return HttpResponse("Database error", content_type="text/plain", status=503)
    return HttpResponse("OK", content_type="text/plain", status=200)