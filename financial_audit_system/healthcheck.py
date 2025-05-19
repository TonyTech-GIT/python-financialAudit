# from django.http import JsonResponse
# from django.views.decorators.http import require_GET
# from django.db import connection

# @require_GET
# def health_check(request):
#     try:
#         # Test database connection
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT 1")
#         return JsonResponse({"status": "ok"}, status=200)
#     except Exception as e:
#         return JsonResponse({"status": "error", "detail": str(e)}, status=500)


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_GET
def health_check(request):
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            
        # Test Redis/cache if you use it
        # from django.core.cache import cache
        # cache.set('healthcheck', 'test', 5)
        
        return JsonResponse({
            "status": "ok",
            "database": "connected"
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "database": str(e)
        }, status=500)