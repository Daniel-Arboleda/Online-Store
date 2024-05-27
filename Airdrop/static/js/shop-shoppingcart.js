
// Este código de JS es para manejar los botones del selector de cantidad de un producto en la página shop.html antes de añadir el producto al carrito mediante el botón correspondiente

function changeQuantity(action, productName) {
    let quantityInput = document.getElementById('quantity-' + productName);
    let currentQuantity = parseInt(quantityInput.value);
    if (action === 'increase') {
        quantityInput.value = currentQuantity + 1;
    } else if (action === 'decrease' && currentQuantity > 1) {
        quantityInput.value = currentQuantity - 1;
    }
    updateCart(productName, parseInt(quantityInput.value)); // Actualiza el carrito con la nueva cantidad
}

// ---------------------------------------

function addToCart(productName, price, image, qty) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    cart[productName] = { price: price, image: image, qty: qty };
    localStorage.setItem('cart', JSON.stringify(cart));
    alert('Producto añadido al carrito');
    displayCart();  // Actualizar el carrito para reflejar los cambios
}

// -------------------------------------------------
// Esto es el código que permite agregar o visualizar los productos seleccionados en la tienda mendiante el botón añadir al carrito en el carrito de compras del desarrollo

function updateCart(productName, newQty) {
    let cart = JSON.parse(localStorage.getItem('cart'));
    if (cart && cart[productName]) {
        if (newQty > 0) {
            cart[productName].qty = newQty;
        } else {
            delete cart[productName]; // Si la cantidad es 0 o menos, elimina el producto del carrito
        }
        localStorage.setItem('cart', JSON.stringify(cart));
        displayCart(); // Refresca la vista del carrito
    }
}




// Código para que el carrito de compras lea los productos desde el almaenamiento local y muestre los productos, por tanto, los productos del carrito se llenarán desde el JavaScript

document.addEventListener('DOMContentLoaded', function() {
    displayCart();
});


// Función que actualiza los valores del carrito de compras y actualiza el valor en el DOM del carrito
function displayCart() {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    let cartItemsContainer = document.querySelector('.cart-items');
    let total = 0;
    let itemCount = 0;  // Inicializa el contador de ítems

    cartItemsContainer.innerHTML = ''; // Limpiar contenedor de ítems del carrito

    for (let productName in cart) {
        const product = cart[productName];
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <img src="${staticUrl + 'img/' + product.image}" alt="${productName}" class="product-image">
            <div class="item-info">
                <h2 class="item-title">${productName}</h2>
                <div class="quantity-control">
                    <button class="quantity-btn" onclick="changeQuantity('increase', '${productName}')">+</button>
                    <input type="number" id="quantity-${productName}" value="${product.qty}" class="item-quantity">
                    <button class="quantity-btn" onclick="changeQuantity('decrease', '${productName}')">-</button>
                </div>
                <p class="item-price">$${(product.price * product.qty).toFixed(2)}</p>
                <button class="remove-item" onclick="removeFromCart('${productName}')">Eliminar</button>
            </div>
        `;
        cartItemsContainer.appendChild(cartItem);
        total += product.price * product.qty;
        itemCount += product.qty;  // Suma la cantidad de cada producto al total de ítems

    }

    document.querySelector('.total-price').textContent = `$${total.toFixed(2)}`;
    document.getElementById('cart-item-count').textContent = itemCount;  // Actualiza el contador de ítems en la página

}



function removeFromCart(productName) {
    let cart = JSON.parse(localStorage.getItem('cart'));
    delete cart[productName];
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCart(); // Actualizar la visualización del carrito
}
