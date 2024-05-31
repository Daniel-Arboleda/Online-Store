// Método en JavaScript para manejar el mensaje emergente que validara la opción de eliminar o conservar el producto en la lista de stock, en caso que sea un error del usuario podra dar click en cancelar la petición


// document.addEventListener('DOMContentLoaded', function() {
//     var deleteButtons = document.querySelectorAll('.btn-delete');

//     deleteButtons.forEach(function(button) {
//         button.addEventListener('click', function() {
//             var productId = this.getAttribute('data-product-id');
//             if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
//                 document.getElementById('delete_form_' + productId).submit();
//             }
//         });
//     });
// });




// Archivo: delete_mess_products.js

// document.addEventListener('DOMContentLoaded', function() {
//     var deleteButtons = document.querySelectorAll('.delete-btn');

//     console.log('Número de botones de eliminación encontrados:', deleteButtons.length);

//     deleteButtons.forEach(function(button) {
//         button.addEventListener('click', function() {
//             console.log('Botón de eliminación clickeado');

//             var formId = this.parentNode.getAttribute('id'); // Obtener el ID del formulario padre
//             var productId = formId.split('_')[2]; // Obtener el ID del producto del ID del formulario

//             if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
//                 console.log('Eliminando producto con ID:', productId);
//                 document.getElementById(formId).submit();
//             }
//         });
//     });
// });




// document.addEventListener('DOMContentLoaded', function() {
//     var deleteButtons = document.querySelectorAll('.delete-btn');

//     console.log('Número de botones de eliminación encontrados:', deleteButtons.length);

//     deleteButtons.forEach(function(button) {
//         button.addEventListener('click', function() {
//             var productId = this.getAttribute('data-product-id');
//             if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
//                 console.log('Eliminando producto con ID:', productId);

//                 // Crear un formulario oculto para enviar la solicitud POST
//                 var form = document.createElement('form');
//                 form.method = 'POST';
//                 form.action = '/products/' + productId + '/delete/';
//                 form.style.display = 'none'; // Ocultar el formulario

//                 // Añadir token CSRF al formulario
//                 var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
//                 var csrfInput = document.createElement('input');
//                 csrfInput.type = 'hidden';
//                 csrfInput.name = 'csrfmiddlewaretoken';
//                 csrfInput.value = csrfToken;
//                 form.appendChild(csrfInput);

//                 document.body.appendChild(form); // Agregar formulario al DOM
//                 form.submit(); // Enviar formulario
//             } else {
//                 console.log('Cancelado');
//                 // Opcional: manejar lo que sucede si el usuario cancela la eliminación
//             }
//         });
//     });
// });





// // Metodo funcional con inclución del token de seguridad CSRF
// document.addEventListener('DOMContentLoaded', function() {
//     var deleteButtons = document.querySelectorAll('.delete-btn');

//     console.log('Número de botones de eliminación encontrados:', deleteButtons.length);

//     deleteButtons.forEach(function(button) {
//         button.addEventListener('click', function() {
//             var productId = this.getAttribute('data-product-id');
//             if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
//                 console.log('Eliminando producto con ID:', productId);

//                 // Crear un formulario oculto para enviar la solicitud POST
//                 var form = document.createElement('form');
//                 form.method = 'POST';
//                 form.action = '/products/' + productId + '/delete/';
//                 form.style.display = 'none'; // Ocultar el formulario

//                 // Añadir token CSRF al formulario
//                 var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
//                 var csrfInput = document.createElement('input');
//                 csrfInput.type = 'hidden';
//                 csrfInput.name = 'csrfmiddlewaretoken';
//                 csrfInput.value = csrfToken;
//                 form.appendChild(csrfInput);

//                 document.body.appendChild(form); // Agregar formulario al DOM
//                 form.submit(); // Enviar formulario
//             } else {
//                 console.log('Cancelado');
//                 // Opcional: manejar lo que sucede si el usuario cancela la eliminación
//             }
//         });
//     });
// });




// Método optimizado de velocidad vara evitar la alerta de rendimiento en la consola del navegador


document.addEventListener('DOMContentLoaded', function() {
    var deleteButtons = document.querySelectorAll('.delete-btn');

    console.log('Número de botones de eliminación encontrados:', deleteButtons.length);

    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var productId = this.getAttribute('data-product-id');
            if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
                console.log('Eliminando producto con ID:', productId);
                
                // Crear y enviar el formulario de eliminación lo más rápido posible
                var form = createDeleteForm(productId);
                document.body.appendChild(form);
                form.submit();
            } else {
                console.log('Cancelado');
            }
        });
    });

    function createDeleteForm(productId) {
        // Crear un formulario oculto para enviar la solicitud POST
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/products/' + productId + '/delete/';
        form.style.display = 'none'; // Ocultar el formulario

        // Añadir token CSRF al formulario
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        var csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);

        return form;
    }
});
