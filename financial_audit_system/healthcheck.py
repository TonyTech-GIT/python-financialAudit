from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_GET
def health_check(request):
    """Enhanced health check with logging"""
    try:
        # Basic web server check
        response = {
            'status': 'OK',
            'service': 'Django',
            'database': 'accessible'
        }
        
        # Database check
        if settings.HEALTHCHECK_ENABLED:
            from django.db import connection
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
            except Exception as e:
                logger.error(f"Database healthcheck failed: {str(e)}")
                response.update({
                    'status': 'ERROR',
                    'database': 'unavailable',
                    'error': str(e)
                })
                return JsonResponse(response, status=503)
        
        return JsonResponse(response, status=200)
    
    except Exception as e:
        logger.critical(f"Healthcheck system failure: {str(e)}")
        return JsonResponse(
            {'status': 'CRITICAL', 'error': str(e)},
            status=500
        )