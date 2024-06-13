document.addEventListener('DOMContentLoaded', function() {
    // Hamburger menu functionality
    var hamburgerMenu = document.querySelector('.hamburger-menu');
    var navMenu = document.querySelector('#navMenu');

    hamburgerMenu.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });
});
