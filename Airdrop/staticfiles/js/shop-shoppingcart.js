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

// Función para agregar productos al carrito
function addToCart(productId, price, imageUrl, quantity, stock) {
    console.log("addToCart called with productId:", productId, "price:", price, "imageUrl:", imageUrl, "quantity:", quantity, "stock", stock);
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const existingProductIndex = cart.findIndex(product => product.id === productId);
    let productAdded = false;

    if (existingProductIndex > -1) {
        const existingProduct = cart[existingProductIndex];
        const newQuantity = existingProduct.quantity + quantity;

        if (newQuantity > stock) {
            alert('No puedes añadir más productos al carrito que el stock disponible');
            existingProduct.quantity = stock;  // Set to max stock if over
        } else {
            existingProduct.quantity = newQuantity;
            productAdded = true;
        }
    } else {
        if (quantity > stock) {
            alert('No puedes añadir más productos que el stock disponible');
        } else {
            cart.push({ id: productId, price: price, imageUrl: imageUrl, quantity: quantity });
            productAdded = true;
        }
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    if (productAdded) {
        alert('Producto añadido al carrito');
    }
    // Restablecer el valor del input de cantidad a 1
    document.getElementById(`quantity-${productId}`).value = 1;
}

// Función para cargar los productos del carrito desde el almacenamiento local y mostrarlos en la página del carrito
document.addEventListener('DOMContentLoaded', function() {
    const cartContainer = document.getElementById('cart-container');
    if (cartContainer) {
        loadCart();
    }
});

function loadCart() {
    console.log("loadCart called");
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    console.log("Cart contents:", cart);
    const cartContainer = document.getElementById('cart-container');
    const cartItemsContainer = cartContainer.querySelector('.cart-items'); // Use the container found within cartContainer
    const cartItemCount = document.getElementById('cart-item-count');
    const totalPriceElement = document.querySelector('.total-price');

    let totalPrice = 0;
    let totalItems = 0;

    cartItemsContainer.innerHTML = ''; // Clear the container

    cart.forEach(product => {
        console.log("Processing product:", product);
        const productTotalPrice = product.price * product.quantity;
        totalPrice += productTotalPrice;
        totalItems += product.quantity;

        const productElement = document.createElement('div');
        productElement.classList.add('cart-item');
        // Aquí estan los elementos que se renderizaran en la tarjeta de cada producto mostrado en el carrito de compras
        productElement.innerHTML = `
            <img src="${product.imageUrl}" alt="Imagen del producto">
            <div class="cart-item-details">
                <h3>Producto ID: ${product.id}</h3>
                <p>Precio: $${product.price}</p>
                <p>Cantidad: ${product.quantity}</p>
                <p>Total: $${productTotalPrice.toFixed(2)}</p>
                <button class="remove-item" onclick="confirmRemoveFromCart('${product.id}')">Eliminar</button>
            </div>
        `;

        cartItemsContainer.appendChild(productElement);
    });

    cartItemCount.textContent = totalItems;
    totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
}

// Función para confirmar la eliminación de un producto del carrito
function confirmRemoveFromCart(productId) {
    console.log(`confirmRemoveFromCart called with productId: ${productId}`);
    const userConfirmed = confirm("¿Estás seguro de que deseas eliminar este producto?");
    if (userConfirmed) {
        removeFromCart(productId);
    } else {
        console.log("Eliminación cancelada por el usuario.");
    }
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

// Call loadCart when the page is loaded
document.addEventListener('DOMContentLoaded', function() {
    const cartContainer = document.getElementById('cart-container');
    if (cartContainer) {
        loadCart();
    }
});
