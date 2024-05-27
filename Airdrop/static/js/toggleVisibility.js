
// ---------------------------------------------------------------




// --------------------------------------------------------------



// ---------------------------------------------------------------


// theme-toggle.js
document.addEventListener('DOMContentLoaded', function() {
    // Asegúrate de que el ID aquí coincide con el ID en tu HTML
    const themeToggle = document.getElementById('theme-toggle');

    themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark_theme');
    });
});


// ---------------------------------------------------------------



// JavaScript para el despliege de los contenedores

function toggleVisibility(header) {
    var content = header.nextElementSibling; // Obtiene el elemento hermano directo, que es el contenido desplegable
    if (content.style.display === "block") {
        content.style.display = "none"; // Oculta el contenido
    } else {
        content.style.display = "block"; // Muestra el contenido
        content.style.overflow = "hidden"; // Asegura que todo el contenido esté dentro del contenedor
    }
}

