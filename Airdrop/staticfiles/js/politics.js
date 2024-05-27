
// Ventaja modal de las politicas de lugares

// Obtiene la ventana emergente y el botón de cierre
var modal = document.getElementById("modal-lugares");
var closeButton = document.querySelector("#modal-lugares .close");

// Muestra la ventana emergente cuando se hace clic en el botón +
function showModal() {
    modal.style.display = "block";
}

// Oculta la ventana emergente cuando se hace clic en el botón de cierre
closeButton.onclick = function() {
    modal.style.display = "none";
}

// Oculta la ventana emergente cuando se hace clic fuera de ella
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}



// -------------------------------------------------------------

