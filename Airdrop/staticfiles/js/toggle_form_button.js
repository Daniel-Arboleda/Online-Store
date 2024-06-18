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
        ['userForm', 'productForm'].forEach(function(formId) {
            var form = document.getElementById(formId);
            if (form) {
                form.classList.toggle('hidden');
            }
        });
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
