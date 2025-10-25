from django.utils.deprecation import MiddlewareMixin

class SimpleLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(f"➡️ Նոր հարցում: {request.method} {request.path}")

    def process_response(self, request, response):
        print(f"⬅️ Պատասխան՝ {response.status_code}")
        return response
    
import logging
import time

logger = logging.getLogger('django.request')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логируем входящий запрос
        logger.info(f"Request: {request.method} {request.get_full_path()} User: {request.user}")

        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        # Логируем ответ и время обработки
        logger.info(
            f"Response: {response.status_code} for {request.method} {request.get_full_path()} "
            f"Duration: {duration:.3f}s"
        )

        return response
