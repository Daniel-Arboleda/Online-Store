// Script para mostrar/ocultar el formulario
// document.getElementById('toggleFormBtn').addEventListener('click', function() {
//     var form = document.getElementById('productForm');
//     if (form.classList.contains('hidden')) {
//         form.classList.remove('hidden');
//     } else {
//         form.classList.add('hidden');
//     }
// });
// implementaremos un script JavaScript que detecte si el código de producto o el nombre del producto ya existen en la base de datos con la función addEventListener, Comparar los campos para saber si son del mismo producto con la función ---- Método para comparar las variables y saber si pertenencen al mismo producto, maneja la lógica de verificación con la función checkProductFields() para que la verificación se realice automáticamente cuando se cambien los campos messageDiv ---- Para cambiar el botón de manera dinámica de Crear a Modificar según la respuesta del servidor creamos la siguiente constante btnORM ---- JavaScript para auto-rellenar los campos del formulario en función de la respuesta del servidor con la creación de las consntantes descriptionInput = document.getElementById('description'); y modificando el checkProductFields usando la nueva variable autofillForm(data.product); en caso de no requerir cambios usara la variable clearForm();
// document.addEventListener('DOMContentLoaded', function() {
//     var codeInput = document.getElementById('code');
//     var nameInput = document.getElementById('name_prod');
//     const messageDiv = document.getElementById('message');
//     const btnORM = document.getElementById('submitButton');
//     const descriptionInput = document.getElementById('description');
//     const priceInput = document.getElementById('price');
//     const stockInput = document.getElementById('stock');
//     const categoriesInput = document.getElementById('categories');
//     const brandInput = document.getElementById('brand');
//     const stateInput = document.getElementById('state');
//     const disponibilityInput = document.getElementById('disponibility');
//     // Toggle form visibility
//     document.getElementById('toggleFormBtn').addEventListener('click', function() {
//         var form = document.getElementById('productForm');
//         form.classList.toggle('hidden');
//     });
    // codeInput.addEventListener('input', function() {
    //     var code = codeInput.value;
    //     if (code){
    //         fetch(`/check_product_existence/?code=${code}`)
    //             .then(response => response.json())
    //             .then(data => {
    //                 if (data.code_exists) {
    //                     console.log('El código existe en la DB');
    //                     return(code);
                        
    //                 } else {
    //                     console.log('El código del producto no existe en la DB');
    //                 }
    //             });
    //     }
    // });
    // nameInput.addEventListener('input', function() {
    //     var name = nameInput.value;
    //     if (name) {
    //         fetch(`/check_product_existence/?name=${name}`)
    //             .then(response => response.json())
    //             .then(data => {
    //                 if (data.name_exists) {
    //                     console.log('El nombre existe en la DB');
    //                     return(name);
    //                 } else {
    //                     console.log('El nombre del producto no existe en la DB');
    //                 }
    //             });
    //     }
    // });
//     function checkProductFields() {
//         const code = codeInput.value;
//         const name = nameInput.value;
//         codeInput.addEventListener('input', function() {
//             var code = codeInput.value;
//             if (code){
//                 fetch(`/check_product_existence/?code=${code}`)
//                     .then(response => response.json())
//                     .then(data => {
//                         if (data.code_exists) {
//                             console.log('El código existe en la DB');
//                             return(code);
                            
//                         } else {
//                             console.log('El código del producto no existe en la DB');
//                         }
//                     });
//             }
//         });
//         nameInput.addEventListener('input', function() {
//             var name = nameInput.value;
//             if (name) {
//                 fetch(`/check_product_existence/?name=${name}`)
//                     .then(response => response.json())
//                     .then(data => {
//                         if (data.name_exists) {
//                             console.log('El nombre existe en la DB');
//                             return(name);
//                         } else {
//                             console.log('El nombre del producto no existe en la DB');
//                         }
//                     });
//             }
//         });

//         if (code && name) {
//             fetch(`/check_product_fields/?code=${code}&name=${name}`)
//                 .then(response => response.json())
//                 .then(data => {
//                     console.log(data.message);
//                     console.log('AAAAAAA');
//                     messageDiv.textContent = data.message;
//                     if (data.message === 'Los campos pertenecen al mismo producto') {
//                         submitButton.textContent = 'Actualizar';
//                         autofillForm(data.product);
//                     } else {
//                         submitButton.textContent = 'Crear';
//                         clearForm();
//                     }
//                 })
//                 .catch(error => {
//                     console.error('Error checking product fields:', error);
//                     console.log('BBBBB');
//                     messageDiv.textContent = 'Error checking product fields';
//                     submitButton.textContent = 'Crear';
//                     clearForm();
//                 });
//         } else {
//             console.log('Código y nombre son requeridos');
//             console.log('CCCCC');
//             messageDiv.textContent = 'Código y nombre son requeridos';
//             submitButton.textContent = 'Crear';
//             clearForm();  
//         }
//     }

//     function autofillForm(product) {
//         descriptionInput.value = product.description;
//         priceInput.value = product.price;
//         stockInput.value = product.stock;
//         categoriesInput.value = product.categories;
//         brandInput.value = product.brand;
//         stateInput.value = product.state;
//         disponibilityInput.value = product.disponibility;
//     }

//     function clearForm() {
//         descriptionInput.value = '';
//         priceInput.value = '';
//         stockInput.value = '';
//         categoriesInput.value = '';
//         brandInput.value = '';
//         stateInput.value = '';
//         disponibilityInput.value = '';
//     }
//     // Add event listeners to the input fields to trigger the check on change
//     codeInput.addEventListener('change', checkProductFields);
//     nameInput.addEventListener('change', checkProductFields);
// });
   

document.addEventListener('DOMContentLoaded', function() {
    const codeInput = document.getElementById('code');
    const nameInput = document.getElementById('name_prod');
    const messageDiv = document.getElementById('message');
    const submitButton = document.getElementById('submitButton');
    const descriptionInput = document.getElementById('description');
    const priceInput = document.getElementById('price');
    const stockInput = document.getElementById('stock');
    const categoriesInput = document.getElementById('categories');
    const brandInput = document.getElementById('brand');
    const stateInput = document.getElementById('state');
    const disponibilityInput = document.getElementById('disponibility');

    document.getElementById('toggleFormBtn').addEventListener('click', function() {
        var form = document.getElementById('productForm');
        form.classList.toggle('hidden');
    });

    codeInput.addEventListener('input', checkProductFields);
    nameInput.addEventListener('input', checkProductFields);

    function checkProductFields() {
        const code = codeInput.value.trim();
        const name = nameInput.value.trim();

        let url = '/get_product_details/?';
        if (code) url += `code=${code}&`;
        if (name) url += `name=${name}`;

        fetch(url)
            .then(response => response.json())
            .then(data => handleResponse(data))
            .catch(error => {
                console.error('Error checking product fields:', error);
                messageDiv.textContent = 'Error verificando los campos del producto';
                submitButton.textContent = 'Crear';
                submitButton.disabled = false;
                clearForm();
            });
    }

    function handleResponse(data) {
        let codeExistsMsg = data.code_exists ? 'El código existe en la DB' : 'El código del producto no existe en la DB';
        let nameExistsMsg = data.name_exists ? 'El nombre existe en la DB' : 'El nombre del producto no existe en la DB';

        console.log(codeExistsMsg);
        console.log(nameExistsMsg);

        messageDiv.textContent = data.message;

        if (data.message === 'Ambos campos son del mismo producto') {
            submitButton.textContent = 'Actualizar';
            submitButton.disabled = false;
            autofillForm(data.product);
        } else {
            submitButton.textContent = 'Crear';
            submitButton.disabled = data.message === 'Los campos pertenecen a productos distintos';
            clearForm();
        }
    }

    function autofillForm(product) {
        if (!product) {
            console.error('Datos del producto faltan.');
            return;
        }

        if (descriptionInput) descriptionInput.value = product.description || '';
        if (priceInput) priceInput.value = product.price || '';
        if (stockInput) stockInput.value = product.stock || '';
        if (categoriesInput) categoriesInput.value = product.categories || '';
        if (brandInput) brandInput.value = product.brand || '';
        if (stateInput) stateInput.value = product.state || '';
        if (disponibilityInput) disponibilityInput.value = product.disponibility || '';
    }

    function clearForm() {
        if (descriptionInput) descriptionInput.value = '';
        if (priceInput) priceInput.value = '';
        if (stockInput) stockInput.value = '';
        if (categoriesInput) categoriesInput.value = '';
        if (brandInput) brandInput.value = '';
        if (stateInput) stateInput.value = '';
        if (disponibilityInput) disponibilityInput.value = '';
    }
});
