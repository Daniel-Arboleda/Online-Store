# middleware.py

import logging

logger = logging.getLogger(__name__)

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/admin/'):  # Verifica si la solicitud es para la interfaz de administración
            logger.info(f"Acceso a la interfaz de administración: {request.method} {request.path} por el usuario {request.user}")

        return response
