from django.http import HttpResponse

def health_check(request):
    """Simplest possible health check that cannot fail"""
    return HttpResponse(status=200)