// Ejemplo de uso con un botón
// document.querySelectorAll('.addtocart').forEach(button => {
//     button.addEventListener('click', function() {
//         const productId = parseInt(this.dataset.productId); // Suponiendo que tienes data-product-id en el botón
//         const productPrice = parseFloat(this.dataset.productPrice);
//         const productImage = this.dataset.productImage;
//         const quantity = getQuantity(productId);
//         const stock = parseInt(this.dataset.stock);
//         const url = this.getAttribute('data-url');

//         // Añadir mensajes de depuración
//         console.log('Datos del botón:');
//         console.log('Product ID:', productId);
//         console.log('Product Price:', productPrice);
//         console.log('Product Image:', productImage);
//         console.log('Quantity:', quantity);
//         console.log('Stock:', stock);

//         addToCart(productId, productPrice, productImage, quantity, stock);
//     });
// });



async function addToCart(productId, productPrice, productImage, quantity, stock, url) {

    // Depuración de los valores de quantity y stock making the request
    console.log('Request quantity:');
    console.log("product_id:", productId);
    console.log("Stock disponible:", quantity);
    console.log("Cantidad solicitada:", stock);

    if (quantity <= stock) {
        // const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
        const csrfElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfElement) {
            console.error('CSRF token not found.');
            return;
        }
        // const csrftoken = csrfElement.value;
        const csrftoken = csrfElement.getAttribute('content');

        console.log("Datos enviados al servidor:");
        console.log("product_id:", productId);
        console.log("quantity:", quantity);
        console.log("productPrice:", productPrice);
        console.log("productImage:", productImage);

        try {
            // const response = await fetch('{% url "add_to_cart" %}', {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity,
                    productPrice: productPrice,  // Opcional
                    productImage: productImage   // Opcional
                })
            });

            const data = await response.json();
            console.log("Respuesta del servidor:", data);
            if (data.success) {
                alert('Producto añadido al carrito.');
                // Actualizar el carrito si es necesario
                loadCart();
            } else {
                alert('Error al añadir el producto al carrito.' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        alert('No hay suficiente stock disponible.');
    }
}

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

document.querySelectorAll('.addtocart').forEach(button => {
    button.addEventListener('click', function() {
        const productId = parseInt(this.getAttribute('data-product-id'));
        const productPrice = parseFloat(this.getAttribute('data-product-price'));
        const productImage = this.getAttribute('data-product-image');
        const stock = parseInt(this.getAttribute('data-stock'));
        const quantity = getQuantity(productId);
        const url = this.getAttribute('data-url');

        // Añadir mensajes de depuración
        console.log('Datos del botón:');
        console.log('Product ID:', productId);
        console.log('Product Price:', productPrice);
        console.log('Product Image:', productImage);
        console.log('Quantity:', quantity);
        console.log('Stock:', stock);

        addToCart(productId, productPrice, productImage, quantity, stock, url);
    });
});

function getQuantity(productId) {
    const quantityInput = document.getElementById(`quantity-${productId}`);
    if (quantityInput) {
        return parseInt(quantityInput.value);
    }
    console.error(`Input de cantidad no encontrado para el producto ID: ${productId}`);
    return 0;
}

// // Ejemplo de uso con un producto
// const exampleProductId = 1; // Obtén esto de alguna manera
// const exampleProductPrice = 10.0; // Obtén esto de alguna manera
// const exampleProductImage = "image_url"; // Obtén esto de alguna manera
// const exampleStock = 5; // Obtén esto de alguna manera
// const exampleQuantity = getQuantity(exampleProductId);

// addToCart(exampleProductId, exampleProductPrice, exampleProductImage, exampleQuantity, exampleStock);

// Función para manejar la cantidad de productos
function changeQuantity(action, productId, stock) {
    console.log("changeQuantity called with action:", action, "productId:", productId, "stock:", stock);
    const quantityInput = document.getElementById(`quantity-${productId}`);
    let currentQuantity = parseInt(quantityInput.value);

    if (action === 'increase' && currentQuantity < stock) {
        currentQuantity += 1;
    } else if (action === 'decrease' && currentQuantity > 1) {
        currentQuantity -= 1;
    } else if (action === 'increase' && currentQuantity >= stock) {
        alert('No puedes seleccionar más productos que el stock disponible');
    }
    quantityInput.value = currentQuantity;
}

document.addEventListener('DOMContentLoaded', function() {
    const cartContainer = document.getElementById('cart-container');
    if (cartContainer) {
        loadCart();
    }
});

function loadCart() {
    fetch('{% url "get_cart_items" %}')  // Asegúrate de tener una vista que devuelva los artículos del carrito
    .then(response => response.json())
    .then(data => {
        const cartItemsContainer = document.querySelector('.cart-items');
        cartItemsContainer.innerHTML = '';  // Clear the container

        data.cart_items.forEach(item => {
            const productElement = document.createElement('div');
            productElement.classList.add('cart-item');
            productElement.innerHTML = `
                <img src="${item.product.imageUrl}" alt="Imagen del producto">
                <div class="cart-item-details">
                    <h3>${item.product.name}</h3>
                    <p>Precio: $${item.price}</p>
                    <p>Cantidad: ${item.quantity}</p>
                    <p>Total: $${item.amount}</p>
                    <button class="remove-item" onclick="removeFromCart('${item.product.id}')">Eliminar</button>
                </div>
            `;
            cartItemsContainer.appendChild(productElement);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function removeFromCart(productId) {
    console.log(`removeFromCart called with productId: ${productId}`);
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const originalLength = cart.length;
    cart = cart.filter(product => product.id !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    const newLength = cart.length;

    if (originalLength > newLength) {
        console.log(`Product with ID: ${productId} removed from cart`);
    } else {
        console.log(`Product with ID: ${productId} not found in cart`);
    }

    loadCart(); // Actualizar la visualización del carrito
}

// Call loadCart when the page is loaded ---- JavaScript para Cargar el Carrito. Aseguramos que el carrito se cargue correctamente cuando el usuario visite la vista del carrito
document.addEventListener('DOMContentLoaded', function() {
    const cartContainer = document.getElementById('cart-container');
    if (cartContainer) {
        loadCart();
    }
});



