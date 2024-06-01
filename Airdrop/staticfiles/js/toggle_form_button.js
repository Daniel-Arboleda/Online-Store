// Script para mostrar/ocultar el formulario
document.getElementById('toggleFormBtn').addEventListener('click', function() {
    var form = document.getElementById('productForm');
    if (form.classList.contains('hidden')) {
        form.classList.remove('hidden');
    } else {
        form.classList.add('hidden');
    }
});


// implementaremos un script JavaScript que detecte si el código de producto o el nombre del producto ya existen en la base de datos con la función addEventListener, Comparar los campos para saber si son del mismo producto con la función ---- Método para comparar las variables y saber si pertenencen al mismo producto, maneja la lógica de verificación con la función checkProductFields() para que la verificación se realice automáticamente cuando se cambien los campos messageDiv 
document.addEventListener('DOMContentLoaded', function() {
    var codeInput = document.getElementById('code');
    var nameInput = document.getElementById('name_prod');
    const messageDiv = document.getElementById('message');

    codeInput.addEventListener('input', function() {
        var code = codeInput.value;
        if (code){
            fetch(`/check_product_existence/?code=${code}`)
                .then(response => response.json())
                .then(data => {
                    if (data.code_exists) {
                        console.log('El código existe en la DB');
                    } else {
                        console.log('El código del producto no existe en la DB');
                    }
                });
        }
    });

    nameInput.addEventListener('input', function() {
        var name = nameInput.value;
        if (name) {
            fetch(`/check_product_existence/?name=${name}`)
                .then(response => response.json())
                .then(data => {
                    if (data.name_exists) {
                        console.log('El nombre existe en la DB');
                    } else {
                        console.log('El nombre del producto no existe en la DB');
                    }
                });
        }
    });

    function checkProductFields() {
        const code = codeInput.value;
        const name = nameInput.value;

        if (code && name) {
            fetch(`/check_product_fields/?code=${code}&name=${name}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                    messageDiv.textContent = data.message;
                })
                .catch(error => {
                    console.error('Error checking product fields:', error);
                    messageDiv.textContent = 'Error checking product fields';
                });
        } else {
            console.log('Código y nombre son requeridos');
            messageDiv.textContent = 'Código y nombre son requeridos';
        }
    }
    // Add event listeners to the input fields to trigger the check on change
    codeInput.addEventListener('change', checkProductFields);
    nameInput.addEventListener('change', checkProductFields);
});
   

// Método para comparar las variables y saber si pertenencen al mismo producto, maneja la lógica de verificación






// Función para auto-rellenar el formulario si se detecta un producto existente
// function autofillForm(product) {
//     formTitle.textContent = 'Actualizar Producto';
//     productIdField.value = product.id;
//     document.getElementById('code').value = product.code;
//     document.getElementById('name').value = product.name;
//     // Rellenar el resto de campos del formulario según sea necesario
//     document.getElementById('description').value = product.description;
//     document.getElementById('price').value = product.price;
//     document.getElementById('stock').value = product.stock;
//     document.getElementById('categories').value = product.categories;
//     document.getElementById('brand').value = product.brand;
//     document.getElementById('state').value = product.state;
//     document.getElementById('disponibility').value = product.disponibility;

//     // Actualizar el botón y la acción del formulario para actualizar
//     formButton.textContent = 'Actualizar';
//     formButton.setAttribute('form', 'orm-prod-form');
//     formButton.setAttribute('formaction', `/update_product/${product.id}`);
//     productForm.classList.remove('hidden');
//     // El campo de la imagen no puede ser rellenado programáticamente por razones de seguridad.
// }

// function clearForm() {
//     document.getElementById('code').value = '';
//     document.getElementById('name').value = '';
//     document.getElementById('descrition').value = '';
//     document.getElementById('price').value = '';
//     document.getElementById('stock').value = '';
//     document.getElementById('categories').value = '';
//     document.getElementById('brand').value = '';
//     document.getElementById('state').value = '';
//     document.getElementById('disponibility').value = '';
// }

// // Lógica para detectar un producto existente
// function checkProductExistence(code, name) {
//     // Lógica para verificar si el producto existe en la base de datos
//     // Esto podría ser una llamada AJAX a tu backend para consultar la base de datos
//     // Aquí un ejemplo simulado:
//     const products = [
//         { id: 1, code: 'P001', name: 'Producto 1', description: 'Descripción 1', price: 100, stock: 10 },
//         { id: 2, code: 'P002', name: 'Producto 2', description: 'Descripción 2', price: 150, stock: 5 }
//     ];

//     // Buscar el producto por código o nombre
//     const existingProduct = products.find(product => product.code === code || product.name === name);
//     if (existingProduct) {
//         autofillForm(existingProduct);
//     }
// }

// // Event listener para el envío del formulario
// formButton.addEventListener('click', function(event) {
//     event.preventDefault();
//     const form = document.getElementById('orm-prod-form');
//     form.submit();
// });

// // Event listener para detectar cambios en el código o nombre del producto
// document.getElementById('code').addEventListener('change', function() {
//     const code = this.value;
//     const name = document.getElementById('name_prod').value;
//     checkProductExistence(code, name);
// });

// document.getElementById('name').addEventListener('change', function() {
//     const name = this.value;
//     const code = document.getElementById('code').value;
//     checkProductExistence(code, name);
// });



// // JavaScript que cambiará dinámicamente el texto del botón y ajustará el comportamiento del formulario según sea necesario
// document.addEventListener('DOMContentLoaded', function() {
//     const productForm = document.getElementById('productForm');
//     const productIdField = document.getElementById('productId');
//     const formTitle = document.getElementById('formTitle');
//     const formButton = document.getElementById('btn-orm-prod-form');

//     // Lógica para detectar cuando se selecciona un producto existente para actualizar
//     function handleProductSelection(productId) {
//         // Mostrar el formulario y cambiar el título
//         productForm.classList.remove('hidden');
//         formTitle.textContent = 'Actualizar Producto';
        
//         // Actualizar el valor del campo productId oculto
//         productIdField.value = productId;
        
//         // Cambiar el texto del botón y ajustar la acción del formulario
//         formButton.textContent = 'Actualizar';
//         formButton.setAttribute('form', 'orm-prod-form'); // Ajustar el formulario para actualizar
//         formButton.setAttribute('formaction', `/update_product/${productId}`); // Ruta para actualizar producto
//     }

//     // Ejemplo de cómo detectar un evento de selección de producto (simulado)
//     // Aquí debes integrar tu propia lógica para detectar cuándo se selecciona un producto existente
//     const productSelect = document.getElementById('productSelect'); // Cambiar por tu selector real
//     productSelect.addEventListener('change', function() {
//         const selectedProductId = productSelect.value; // Obtener el ID del producto seleccionado
//         handleProductSelection(selectedProductId); // Llamar a la función para manejar la selección
//     });

//     // Event listener para el envío del formulario
//     formButton.addEventListener('click', function(event) {
//         event.preventDefault(); // Prevenir envío por defecto, ya que el formulario se envía dinámicamente
//         const form = document.getElementById('orm-prod-form');
//         form.submit(); // Enviar formulario
//     });
// });

