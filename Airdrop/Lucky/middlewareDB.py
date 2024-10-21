import sqlite3
from django.conf import settings
from django.http import JsonResponse
from django.db import connections

class SQLiteAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Primero, autenticar al usuario desde SQLite3
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            # Conectar a la base de datos SQLite3
            conn = sqlite3.connect(settings.DATABASES['luckycart']['NAME'])
            cursor = conn.cursor()

            # Verificar si el usuario existe
            cursor.execute("SELECT * FROM Auth WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                # Usuario autenticado correctamente, asignar la sesión
                # Aquí podrías guardar la sesión o realizar la lógica para crear un 'player'
                request.user_authenticated = True  # Marcar como autenticado
            else:
                return JsonResponse({"error": "Usuario o contraseña incorrectos"}, status=401)

            # Cerrar conexión SQLite3
            conn.close()

        # Continuar con el siguiente middleware o vista
        response = self.get_response(request)
        return response
