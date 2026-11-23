from django.http import HttpResponse


class HealthCheckMiddleware:
    """Answer kamal-proxy's /up health check before host validation.

    kamal-proxy calls the container directly (Host is the container address,
    not inulty.com), so this has to run ahead of anything that checks
    ALLOWED_HOSTS. That lets ALLOWED_HOSTS stay strict instead of '*'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/up":
            return HttpResponse("OK", content_type="text/plain")
        return self.get_response(request)
