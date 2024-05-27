document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const homeLink = document.getElementById('home-link');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Detiene el envío natural del formulario

        // Aquí puedes agregar lógica de validación o cualquier otra verificación
        // Ejemplo: Validar que el usuario y contraseña sean correctos
        // Si todo está correcto, redirige a 'home'
        window.location.href = homeLink.href;
    });
});