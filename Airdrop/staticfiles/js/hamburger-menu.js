document.addEventListener('DOMContentLoaded', function() {
    var hamburgerMenu = document.querySelector('.hamburger-menu');
    var navMenu = document.querySelector('nav ul');
    
    // Selecciona todos los elementos .dropdown que contienen submenús
    var dropdowns = document.querySelectorAll('.dropdown');

    // Variable para almacenar el temporizador
    var submenuTimer;

    // Función para cerrar todos los submenús
    function closeAllDropdowns() {
        dropdowns.forEach(function(dropdown) {
            dropdown.classList.remove('active');
        });
    }

    hamburgerMenu.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        closeAllDropdowns(); // Asegura que al abrir el menú hamburguesa, se cierran todos los submenús
    });

    // Mostrar submenú cuando se pasa el cursor sobre el ícono o área ampliada
    dropdowns.forEach(function(dropdown) {
        var icon = dropdown.querySelector('a');
        var submenu = dropdown.querySelector('.dropdown-content');
        var dropdownParentLi = dropdown.closest('li'); // Obtener el elemento <li> contenedor

        // Mostrar submenú cuando se pasa el cursor sobre el ícono o área ampliada
        dropdownParentLi.addEventListener('mouseenter', function() {
            closeAllDropdowns(); // Cerrar todos los submenús antes de abrir el nuevo
            dropdown.classList.add('active');
            clearTimeout(submenuTimer); // Limpiar el temporizador si está activo
        });

        // Cerrar submenú después de un pequeño retraso cuando se mueve el cursor fuera
        dropdown.addEventListener('mouseleave', function() {
            submenuTimer = setTimeout(function() {
                dropdown.classList.remove('active');
            }, 300); // Ajusta el tiempo de espera según sea necesario
        });

        // Mantener submenú abierto cuando el cursor se mueve al submenú
        submenu.addEventListener('mouseenter', function() {
            clearTimeout(submenuTimer); // Limpiar el temporizador para cerrar el submenú
        });

        // Cerrar submenú si el cursor sale del submenú
        submenu.addEventListener('mouseleave', function() {
            submenuTimer = setTimeout(function() {
                dropdown.classList.remove('active');
            }, 800); // Ajusta el tiempo de espera según sea necesario
        });
    });

    // Cerrar todos los submenús al hacer clic fuera del menú
    document.addEventListener('click', function(e) {
        if (!navMenu.contains(e.target)) {
            closeAllDropdowns();
        }
    });
});
