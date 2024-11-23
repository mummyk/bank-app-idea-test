# middleware.py
import logging


logger = logging.getLogger(__name__)


class LogUserIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        logger.info(f'User IP: {ip}')

        response = self.get_response(request)

        return response
