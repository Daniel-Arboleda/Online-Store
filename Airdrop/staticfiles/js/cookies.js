

// Obtiene el botón para abrir la ventana emergente y la ventana emergente misma

document.addEventListener("DOMContentLoaded", function() {
    var openModalButton = document.getElementById("openModalButton");
    var modal = document.getElementById("modal-lugares");
    var closeButton = document.querySelector("#modal-lugares .close");
    var confirmButtonLugares = document.getElementById("confirmButton-lugares");
    var modalSegundaVentana = document.getElementById("modal-segunda-ventana");

    // Función para mostrar la ventana emergente
    function showModal() {
        modal.style.display = "block";
    }

    // Función para cerrar la ventana emergente
    function closeModal() {
        modal.style.display = "none";
    }

    // Función para mostrar la segunda ventana emergente
    function showSegundaVentanaModal() {
        modalSegundaVentana.style.display = "block";
    }

    // Event listener para abrir la ventana emergente cuando se hace clic en el botón
    openModalButton.addEventListener("click", showModal);

    
    // Event listener para cerrar la ventana emergente cuando se hace clic en el botón de cierre
    closeButton.addEventListener("click", closeModal);

    // Event listener para cerrar la ventana emergente cuando se hace clic fuera de ella
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            closeModal();
        }
    });

    // Event listener para abrir la segunda ventana emergente cuando se hace clic en el botón "Entiendo y deseo continuar"
    confirmButtonLugares.addEventListener("click", function() {
        closeModal(); // Cerrar la primera ventana emergente
        showSegundaVentanaModal(); // Mostrar la segunda ventana emergente

       
    });
});


// ----------------------------------------------------------------

// Codigo java para la ventana emergente de las cookies de la pagina index, debe abrir la ventana emergente siempre que el usuario cargue la ppagina principal del desarrollo.


// PRimero agrego los botones o eventos que se van a configurar en el codigo
document.addEventListener("DOMContentLoaded", function() {
    var cookieModal = document.getElementById("cookie-modal");
    var acceptButton = document.getElementById("accept-btn");
    var closeButton = document.querySelector("#cookie-modal .close");

    // Mostrar la ventana emergente de cookies
    cookieModal.style.display = "block";

    // Evento para cerrar el modal de cookies
    closeButton.addEventListener("click", function() {
        cookieModal.style.display = "none";
    });
    // Evento para el botón Aceptar todo
    acceptButton.addEventListener("click", function() {
        cookieModal.style.display = "none";
    });

});
