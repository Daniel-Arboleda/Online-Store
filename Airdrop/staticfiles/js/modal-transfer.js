document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("openModal");
    var span = document.querySelector(".close-transfer");
    var confirmYes = document.getElementById("confirmYes");
    var confirmNo = document.getElementById("confirmNo");

    console.log("JavaScript cargado"); // Para depuración

    btn.onclick = function() {
        modal.style.display = "block";
    };

    span.onclick = function() {
        modal.style.display = "none";
    };

    confirmYes.onclick = function() {
        console.log("Transacción confirmada");
        modal.style.display = "none";

        // Obtener el valor del formulario
        const amount = document.getElementById("amount").value;
        const bankName = document.querySelector("input[name='bankName']").value;
        const accountNumber = document.querySelector("input[name='accountNumber']").value;

        // Validar los valores obtenidos antes de redirigir
        if (amount && bankName && accountNumber) {
            const url = `/transfer_form/?amount=${amount}&bankName=${encodeURIComponent(bankName)}&accountNumber=${encodeURIComponent(accountNumber)}`;
            window.location.href = url;
        } else {
            alert("Por favor, complete todos los campos requeridos.");
        }
    };

    confirmNo.onclick = function() {
        console.log("Transacción cancelada");
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});

// Modal para el botón cancelar
document.addEventListener('DOMContentLoaded', function() {
    var cancelModal = document.getElementById("cancelModal");
    var cancelButton = document.querySelector(".cancel-btn");
    var closeCancelModal = document.querySelector(".cancel-close");
    var cancelYes = document.getElementById("cancelYes");
    var cancelNo = document.getElementById("cancelNo");

    // Abre la ventana modal de cancelación
    cancelButton.onclick = function() {
        cancelModal.style.display = "block";
    };

    // Cierra la ventana modal con la cruz
    closeCancelModal.onclick = function() {
        cancelModal.style.display = "none";
    };

    // Botón 'Sí' en la ventana modal de cancelación
    cancelYes.onclick = function() {
        console.log("Operación cancelada");
        cancelModal.style.display = "none";
        // Aquí puedes agregar más código para realizar acciones después de la cancelación
        window.location.href = cancelYes.getAttribute('data-url'); // Assumes data-url is correctly set in the HTML
    };

    // Botón 'No' simplemente cierra la ventana modal
    cancelNo.onclick = function() {
        cancelModal.style.display = "none";
    };

    // Cierra el modal al hacer clic fuera del contenido
    window.onclick = function(event) {
        if (event.target == cancelModal) {
            cancelModal.style.display = "none";
        }
    };
});

// SCRIP para la confirmación de la ventana modal al dar click en el botón Finalizar Transacción en la página transfer_form.html
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('confirmationModal');
    const closeModal = modal.querySelector('.close-transfer');
    const confirmBtn = document.getElementById('confirmTransaction');
    const denyBtn = document.getElementById('denyTransaction');
    const finishTransactionBtn = document.querySelector('.transfer-form-btn');  // Asegúrate de que esta clase corresponde al botón que abre la modal

    finishTransactionBtn.addEventListener('click', function(event) {
        event.preventDefault();  // Previene la acción por defecto (enviar el formulario)
        modal.style.display = 'block';  // Muestra la ventana modal
    });

    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    confirmBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        window.location.href = confirmBtn.getAttribute('data-url');  // Redirige a la URL del atributo data-url
    });

    denyBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Cierra la ventana modal al hacer clic fuera de ella
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});

// ScRIPT para el botoón aceptar de la vantana modal del la acción del botón Finalizar Transacción en el formulario de transfer_form.html el cual debe enviar la información del formulario en el POST para actualizar los fondos de la Wallet en la DB


document.getElementById('confirmTransaction').addEventListener('click', function () {
    const form = document.querySelector('form');
    const url = this.getAttribute('data-url');
    
    // Crear un formulario temporal para enviar los datos
    const tempForm = document.createElement('form');
    tempForm.method = 'POST';
    tempForm.action = url;

    // Añadir el token CSRF
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    tempForm.appendChild(csrfInput);

    // Copiar todos los campos del formulario original al formulario temporal
    new FormData(form).forEach((value, name) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = value;
        tempForm.appendChild(input);
    });

    document.body.appendChild(tempForm);
    tempForm.submit();
});

document.getElementById('denyTransaction').addEventListener('click', function () {
    document.getElementById('confirmationModal').style.display = 'none';
});






// Script para que redirija a la página transfer.html cuando el usuario necesite cargar saldo a la página hacciendo click en el botón del menu superior principal marcado con un icono de +
document.addEventListener('DOMContentLoaded', function() {
    var openModalButton = document.getElementById('openModalButton');
    openModalButton.addEventListener('click', function() {
        var url = this.getAttribute('data-url');  // Obtiene la URL del atributo data-url del botón
        window.location.href = url;  // Redirige a la URL
    });
});

// JavaScript para manejar la presentación del formulario y la actualización del saldo
document.addEventListener('DOMContentLoaded', function() {
    const confirmBtn = document.getElementById('confirmTransaction');
    confirmBtn.addEventListener('click', function() {
        const form = document.getElementById('paymentForm'); // Asegúrate de que este es el ID correcto de tu formulario
        const formData = new FormData(form);
        fetch("{% url 'process_transfer' %}", { // Cambia 'process_transfer' por la URL real que procesa el formulario
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Asegúrate de manejar la protección CSRF
            }
        }).then(response => response.json())
          .then(data => {
              if(data.success) {
                  document.querySelector('.saldo-box p').textContent = '$ ' + data.new_balance;
                  document.getElementById('confirmationModal').style.display = 'none';
              } else {
                  alert('Hubo un error al procesar la transacción.');
              }
          }).catch(error => {
              console.error('Error:', error);
          });
    });
});

// Función auxiliar para obtener el token CSRF desde las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
