
// ruleta.js

document.addEventListener("DOMContentLoaded", function() {
    const ruleta = document.querySelector('.ruleta');
    const startButton = document.getElementById('start-game-btn');
    let spinning = false;

    // Función para iniciar el giro de la ruleta
    function startSpinning() {
        if (!spinning) {
            ruleta.style.animation = 'giro 5s infinite linear';
            spinning = true;
        }
    }

    // Función para detener el giro de la ruleta
    function stopSpinning() {
        ruleta.style.animation = 'none';
        spinning = false;
    }

    // Detener la ruleta al cargar la página
    stopSpinning();

    // Event listener para el botón de iniciar juego
    startButton.addEventListener('click', function() {
        if (spinning) {
            stopSpinning();
        } else {
            startSpinning();
        }
    });
});

