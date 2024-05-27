document.getElementById('start-game-btn').addEventListener('click', function() {
    var ruletaContainer = document.querySelector('.ruleta-container');
    let width = ruletaContainer.scrollWidth / 2; // La mitad porque el contenido está duplicado
    let currentPosition = 0;
    let speed = 10; // Velocidad de desplazamiento

    function move() {
        if (currentPosition < width) {
            currentPosition += speed;
            if (currentPosition >= width) {
                currentPosition = 0;
            }
            ruletaContainer.style.transform = `translateX(-${currentPosition}px)`;
        } else {
            currentPosition = 0;
            ruletaContainer.style.transform = 'translateX(0)';
        }
        requestAnimationFrame(move);
    }

    move();

    // Supongamos que determinas el index así (deberás ajustar esta lógica para que funcione con tu configuración específica)
    setTimeout(() => {
        showWinningModal(currentPosition);
    }, 10000); // Detén la animación después de 10 segundos
});

function showWinningModal(finalPosition) {
    var ruletaContainer = document.querySelector('.ruleta-container');
    var winningModal = document.getElementById('winningModal');
    var prizeName = document.getElementById('prizeName');
    var closeModWin = document.querySelector('.close-mod-win');

    // Calcular cuál opción está en la posición final
    let options = document.querySelectorAll('.opcion-ruleta');
    let index = Math.floor(finalPosition / options[0].offsetWidth) % options.length;

    // Configurar el nombre del premio en la modal
    prizeName.textContent = options[index].textContent;

    // Mostrar la ventana modal
    winningModal.style.display = 'block';

    // Cerrar la ventana modal con el botón de cerrar
    closeModWin.onclick = function() {
        winningModal.style.display = 'none';
    };

    // Cerrar la ventana modal al hacer clic fuera de ella
    window.onclick = function(event) {
        if (event.target == winningModal) {
            winningModal.style.display = 'none';
        }
    };
}
