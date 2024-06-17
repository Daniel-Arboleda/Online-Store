// theme-toggle.js
document.addEventListener('DOMContentLoaded', function() {
    // Asegúrate de que el ID aquí coincide con el ID en tu HTML
    const themeToggle = document.getElementById('theme-toggle');

    themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark_theme');
    });
});
