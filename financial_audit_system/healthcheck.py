from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError

@csrf_exempt
@require_GET
def health_check(request):
    checks = {
        'database': False,
        'status': 'healthy'
    }
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            if cursor.fetchone()[0] == 1:
                checks['database'] = True
    except DatabaseError as e:
        checks['status'] = 'unhealthy'
        checks['database_error'] = str(e)
    
    status_code = 200 if checks['status'] == 'healthy' else 503
    return JsonResponse(checks, status=status_code)