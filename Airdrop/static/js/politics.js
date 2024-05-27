
// Ventaja modal de las politicas de lugares
document.addEventListener('DOMContentLoaded', function() {

    // Obtiene la ventana emergente y el botón de cierre
    var modal = document.getElementById("modal-lugares");
    var closeButton = document.querySelector("#modal-lugares .close");
    var deliveryIcon = document.getElementById("delivery-icon");
    var continueButton = document.getElementById("confirmButton-lugares");

    // Función para mostrar la modal
    deliveryIcon.addEventListener('click', function() {
        modal.style.display = "block";
    });

    // Muestra la ventana emergente cuando se hace clic en el botón +
    function showModal() {
        modal.style.display = "block";
    };
    // Muestra la ventana emergente automáticamente al cargar la página
    // showModal();

    // Oculta la ventana emergente cuando se hace clic en el botón de cierre
    closeButton.onclick = function() {
        modal.style.display = "none";
    };

    // Oculta la ventana emergente cuando se hace clic fuera de ella
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    // Redirige al usuario cuando hace clic en "Entiendo y deseo continuar"
    continueButton.addEventListener('click', function() {
        window.location.href = continueButton.getAttribute('data-url'); // Usa el valor de data-url para la redirección
    });

});


// -------------------------------------------------------------

