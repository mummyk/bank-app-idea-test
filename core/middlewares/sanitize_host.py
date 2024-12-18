class SanitizeHostMiddleware:
    """
       Sanitize host middleware for the given host name/ip address
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_HOST', '')
        # print('Host: %s' % host)
        if ',' in host:
            request.META['HTTP_HOST'] = host.split(',')[0].strip()
        return self.get_response(request)
