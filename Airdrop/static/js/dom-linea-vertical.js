// Obtener referencia a la línea
const lineaVertical = document.getElementById('linea-vertical');

// Leer los atributos
const position = lineaVertical.getAttribute('data-position');
const color = lineaVertical.getAttribute('data-color');

console.log(position); // Muestra "100px"
console.log(color); // Muestra "red"

// Modificar los atributos
lineaVertical.setAttribute('data-position', '150px');
lineaVertical.setAttribute('data-color', 'blue');

// Aplicar los cambios a los estilos si es necesario
lineaVertical.style.left = lineaVertical.getAttribute('data-position');
lineaVertical.style.backgroundColor = lineaVertical.getAttribute('data-color');


// Función para cambiar color al hacer clic
lineaVertical.addEventListener('click', function() {
    this.setAttribute('data-color', 'green');
    this.style.backgroundColor = this.getAttribute('data-color');
});

document.addEventListener('DOMContentLoaded', function() {
    const lineaVertical = document.getElementById('linea-vertical');
    let isDragging = false; // Estado de arrastre

    lineaVertical.addEventListener('mousedown', function(event) {
        isDragging = true;
        this.style.cursor = 'ew-resize';
    });

    window.addEventListener('mousemove', function(event) {
        if (isDragging) {
            const newLeft = event.clientX;
            lineaVertical.style.left = `${newLeft}px`;
            lineaVertical.setAttribute('data-position', `${newLeft}px`);
        }
    });

    window.addEventListener('mouseup', function(event) {
        if (isDragging) {
            lineaVertical.style.cursor = 'default';
            isDragging = false;
        }
    });
});



// Función para actualizar el valor mostrado en el span
function updateLinePositionDisplay() {
    const lineaVertical = document.getElementById('linea-vertical');
    const linePositionDisplay = document.getElementById('linePosition');
    const position = lineaVertical.getAttribute('data-position');

    linePositionDisplay.textContent = position; // Actualiza el texto del span con el valor actual
}

// Llamar a la función al cargar la página
window.onload = function() {
    updateLinePositionDisplay();

    // Suponiendo que quieras actualizar la posición dinámicamente
    const lineaVertical = document.getElementById('linea-vertical');
    lineaVertical.addEventListener('click', function(event) {
        // Solo un ejemplo: mover la línea 10px más a la derecha cada clic
        const currentPosition = parseInt(this.getAttribute('data-position')) || 0;
        const newPosition = currentPosition + 10 + 'px';
        this.setAttribute('data-position', newPosition);
        this.style.left = newPosition;
        updateLinePositionDisplay(); // Actualizar el display cada vez que la posición cambia
    });
};
