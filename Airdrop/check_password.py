import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lucky.settings')
django.setup()

from Lucky.models import CustomUser
from django.contrib.auth import authenticate

try:
    # Verifica el hashing de la contraseña
    user = CustomUser.objects.get(email='core2@core.co')
    print(f"Password hash: {user.password}")

    # Verifica que la contraseña es correcta
    is_correct = user.check_password('12345678Daniel')
    print(f"Is password correct: {is_correct}")

    # Prueba la autenticación
    email = 'core2@core.co'
    password = '12345678Daniel'
    user = authenticate(username=email, password=password)
    print(f"Authenticated user: {user}")

except CustomUser.DoesNotExist:
    print("User does not exist")
