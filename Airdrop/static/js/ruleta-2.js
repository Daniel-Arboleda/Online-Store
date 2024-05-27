// Técnica de animación "Cinta transportadora" así cuando el deplazamiento llegue al final del primer conjunto, inmediatamente comience desde el inicio sin que el usuario perciba interrupciones.
// resetear la posición una vez que se haya alcanzado la mitad del contenedor (ya que los contenidos están duplicados), creando un efecto de bucle continuo.


// Solo duplicar el contenido una vez cuando se carga la página
window.onload = function() {
    var ruletaContainer = document.querySelector('.ruleta-container');
    if (!ruletaContainer.dataset.isDuplicated) {
        var content = ruletaContainer.innerHTML;
        ruletaContainer.innerHTML += content;
        ruletaContainer.dataset.isDuplicated = "true";
    }
};

let currentPosition = 0; // Define currentPosition fuera del evento click para mantener su estado entre clics
let animationFrameId; // Guardar el ID del frame de animación para poder cancelarlo


document.getElementById('start-game-btn').addEventListener('click', function() {
    var ruletaContainer = document.querySelector('.ruleta-container');
    let width = ruletaContainer.scrollWidth / 2; // Ancho del contenido duplicado
    let speed = 10; // Velocidad de desplazamiento
    let animationTime = 6000; // Tiempo de animación en milisegundos
    let startTime = Date.now(); // Tiempo de inicio

    // Cancelar cualquier animación previa que aún esté corriendo
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
    }

    function move() {
        let elapsedTime = Date.now() - startTime;
        if (elapsedTime < animationTime) { // Continuar la animación
            currentPosition += speed; // Incrementa la posición por la velocidad
            if (currentPosition >= width) {
                currentPosition -= width; // Mantiene la animación en la zona visible
            }
            ruletaContainer.style.transform = `translateX(-${currentPosition}px)`;
            animationFrameId = requestAnimationFrame(move); // Continúa la animación
        } else {
            cancelAnimationFrame(animationFrameId); // Detiene la animación
            determineWinner(); // Determina el ganador al final de la animación
        }
    }
    move(); // Inicia la animación
});


function updateLivePosition() {
    const ruletaContainer = document.querySelector('.ruleta-container');
    const containerRect = ruletaContainer.getBoundingClientRect();
    const viewportCenter = window.innerWidth / 2; // Centro del viewport

    const centerPoint = viewportCenter - containerRect.left + ruletaContainer.scrollLeft;
    document.getElementById('livePositionName').textContent = centerPoint.toFixed(2); // Mostrando la posición con dos decimales
}

function move() {
    let elapsedTime = Date.now() - startTime;
    if (elapsedTime < animationTime) {
        currentPosition += speed;
        if (currentPosition >= width) {
            currentPosition -= width;
        }
        ruletaContainer.style.transform = `translateX(-${currentPosition}px)`;
        updateLivePosition();  // Actualiza la posición en tiempo real
        updateLivePreview();  // Actualiza el producto actual si es necesario
        animationFrameId = requestAnimationFrame(move);
    } else {
        cancelAnimationFrame(animationFrameId);
        determineWinner();
    }
}

document.getElementById('start-game-btn').addEventListener('click', function() {
    startPositioning();
    move();
});

function startPositioning() {
    startTime = Date.now();
}

// También asegúrate de inicializar la posición en la carga de la página
window.onload = function() {
    if (!document.querySelector('.ruleta-container').dataset.isDuplicated) {
        var content = document.querySelector('.ruleta-container').innerHTML;
        document.querySelector('.ruleta-container').innerHTML += content;
        document.querySelector('.ruleta-container').dataset.isDuplicated = "true";
    }
    updateLivePosition(); // Asegúrate de que la posición se muestra correctamente al cargar
};




function determineWinner() {
    const ruletaContainer = document.querySelector('.ruleta-container');
    const options = document.querySelectorAll('.opcion-ruleta');
    const optionWidth = options[0].offsetWidth;
    const containerRect = ruletaContainer.getBoundingClientRect();
    const viewportCenter = window.innerWidth / 2; // Centro del viewport
    
    // Calcular el centro visual de la ruleta en relación con el viewport
    const centerPoint = viewportCenter - containerRect.left + ruletaContainer.scrollLeft;

    // Ajustar para asegurar que consideramos el scroll actual del contenedor
    let adjustedCenterPoint = (centerPoint + currentPosition) % (optionWidth * options.length);
    
    // Calcular el índice de la opción bajo la línea central
    let winningOptionIndex = Math.floor(adjustedCenterPoint / optionWidth) % options.length;
    let winningOption = options[winningOptionIndex];

    let winningProductName = winningOption.querySelector('.nombre-op-rul-game').textContent;
    showWinningModal(winningProductName);
}



function showWinningModal(prize) {
    let modal = document.getElementById('winningModal');
    let prizeName = document.getElementById('prizeName');
    let closeModWin = document.querySelector('.close-mod-win');

    prizeName.textContent = prize;
    modal.style.display = "block";

    closeModWin.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}


