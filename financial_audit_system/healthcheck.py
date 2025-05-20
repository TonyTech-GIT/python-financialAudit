from django.http import HttpResponse

def health_check(request):
    """The most basic health check possible"""
    return HttpResponse("OK")