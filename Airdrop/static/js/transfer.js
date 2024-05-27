
// // Método para seeecionar el monto de transferencia
// function toggleCustomAmount(select) {
//     var customAmountInput = document.getElementById('customAmount');
//     if (select.value === 'custom') {
//         customAmountInput.style.display = 'block';
//     } else {
//         customAmountInput.style.display = 'none';
//     }
// }


// // Método para seleccionar el tipo del medio de pago
// function changePaymentMethod(method) {
//     var cardInfo = document.getElementById('creditCardInfo');
//     if (method === 'credit_card') {
//         cardInfo.style.display = 'block';
//     } else {
//         cardInfo.style.display = 'none';
//     }
// }


// Este script manejará la funcionalidad de expandir y colapsar cada sección del formulario al hacer clic en los botones.
function toggleAccordion(accordionId) {
    var accordion = document.getElementById(accordionId);
    var allPanels = document.querySelectorAll('.accordion-content');

    // Cierra todos los paneles excepto el que se quiere alternar
    allPanels.forEach(panel => {
        if (panel.id !== accordionId) {
            panel.style.display = 'none';
        }
    });

    // Alternar la visibilidad del panel seleccionado
    if (accordion.style.display === "block") {
        accordion.style.display = "none";
    } else {
        accordion.style.display = "block";
    }
}



// Funcionamiento del boton cancelar operación en las transacciones

function cancelTransaction() {
    var form = document.getElementById('paymentForm');
    form.reset();  // Esto limpiará todos los campos del formulario.
    var modal = document.getElementById('myModal');
    modal.style.display = 'none';  // Esto cerrará la ventana modal si está abierta.
}


// Código para redirigir a cada una de las paginas de los diversos métodos de pago, cuando el usuario da click en el botón del método deseado en la página de transfer.html
document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.accordion-toggle');
    
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var url = this.getAttribute('data-url'); // Obtiene la URL del atributo data-url del botón
            if (url) {
                window.location.href = url; // Redirige a la URL
            }
        });
    });
});

function toggleRedirection(detailId) {
    var accContent = document.getElementById(detailId);
    accContent.style.display = accContent.style.display === 'block' ? 'none' : 'block';
}






// -----------------------------------------------------------------------------

// Sección reservada para el scrit de redirección a recarga de saldo desde el boton "reargar saldo de la billetera o monedero virtual de la aplicación"

document.addEventListener('DOMContentLoaded', function() {
    const recargarSaldoBtn = document.getElementById('recargarSaldoBtn');

    recargarSaldoBtn.addEventListener('click', function() {
        const url = this.getAttribute('data-url'); // Obtiene la URL del atributo data-url
        window.location.href = url; // Redirige al usuario a la URL
    });
});
