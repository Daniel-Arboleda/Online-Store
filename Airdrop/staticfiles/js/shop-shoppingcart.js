
// Este código de JS es para manejar los botones del selector de cantidad de un producto en la página shop.html antes de añadir el producto al carrito mediante el botón correspondiente

// function changeQuantity(action, productName) {
//     let quantityInput = document.getElementById('quantity-' + productName);
//     let currentQuantity = parseInt(quantityInput.value);
//     if (action === 'increase') {
//         quantityInput.value = currentQuantity + 1;
//     } else if (action === 'decrease' && currentQuantity > 1) {
//         quantityInput.value = currentQuantity - 1;
//     }
//     updateCart(productName, parseInt(quantityInput.value)); // Actualiza el carrito con la nueva cantidad
// }

// // ---------------------------------------

// function addToCart(productName, price, image, qty) {
//     let cart = JSON.parse(localStorage.getItem('cart')) || {};
//     cart[productName] = { price: price, image: image, qty: qty };
//     localStorage.setItem('cart', JSON.stringify(cart));
//     alert('Producto añadido al carrito');
//     displayCart();  // Actualizar el carrito para reflejar los cambios
// }

// -------------------------------------------------
// Esto es el código que permite agregar o visualizar los productos seleccionados en la tienda mendiante el botón añadir al carrito en el carrito de compras del desarrollo

// function updateCart(productName, newQty) {
//     let cart = JSON.parse(localStorage.getItem('cart'));
//     if (cart && cart[productName]) {
//         if (newQty > 0) {
//             cart[productName].qty = newQty;
//         } else {
//             delete cart[productName]; // Si la cantidad es 0 o menos, elimina el producto del carrito
//         }
//         localStorage.setItem('cart', JSON.stringify(cart));
//         displayCart(); // Refresca la vista del carrito
//     }
// }




// Código para que el carrito de compras lea los productos desde el almaenamiento local y muestre los productos, por tanto, los productos del carrito se llenarán desde el JavaScript

// document.addEventListener('DOMContentLoaded', function() {
//     displayCart();
// });

// Función que actualiza los valores del carrito de compras y actualiza el valor en el DOM del carrito
// function displayCart() {
//     let cart = JSON.parse(localStorage.getItem('cart')) || {};
//     let cartItemsContainer = document.querySelector('.cart-items');
//     let total = 0;
//     let itemCount = 0;  // Inicializa el contador de ítems

//     cartItemsContainer.innerHTML = ''; // Limpiar contenedor de ítems del carrito

//     for (let productName in cart) {
//         const product = cart[productName];
//         const cartItem = document.createElement('div');
//         cartItem.classList.add('cart-item');
//         cartItem.innerHTML = `
//             <img src="${staticUrl + 'img/' + product.image}" alt="${productName}" class="product-image">
//             <div class="item-info">
//                 <h2 class="item-title">${productName}</h2>
//                 <div class="quantity-control">
//                     <button class="quantity-btn" onclick="changeQuantity('increase', '${productName}')">+</button>
//                     <input type="number" id="quantity-${productName}" value="${product.qty}" class="item-quantity">
//                     <button class="quantity-btn" onclick="changeQuantity('decrease', '${productName}')">-</button>
//                 </div>
//                 <p class="item-price">$${(product.price * product.qty).toFixed(2)}</p>
//                 <button class="remove-item" onclick="removeFromCart('${productName}')">Eliminar</button>
//             </div>
//         `;
//         cartItemsContainer.appendChild(cartItem);
//         total += product.price * product.qty;
//         itemCount += product.qty;  // Suma la cantidad de cada producto al total de ítems

//     }

//     document.querySelector('.total-price').textContent = `$${total.toFixed(2)}`;
//     document.getElementById('cart-item-count').textContent = itemCount;  // Actualiza el contador de ítems en la página

// }


// function removeFromCart(productName) {
//     let cart = JSON.parse(localStorage.getItem('cart'));
//     delete cart[productName];
//     localStorage.setItem('cart', JSON.stringify(cart));
//     displayCart(); // Actualizar la visualización del carrito
// }







// Método para manejar el incremento y descremento de productos como tambien el botón agregar al carrito con el manejo de la tienda nueva basada en las lecturas de los productos de la DB 


// // shop-shoppingcart.js
// function changeQuantity(action, productId) {
//     const quantityInput = document.getElementById(`quantity-${productId}`);
//     let currentQuantity = parseInt(quantityInput.value);
    
//     if (action === 'increase') {
//         currentQuantity += 1;
//     } else if (action === 'decrease' && currentQuantity > 1) {
//         currentQuantity -= 1;
//     }
    
//     quantityInput.value = currentQuantity;
// }

// function addToCart(productId, price, imageUrl, quantity) {
//     const cart = JSON.parse(localStorage.getItem('cart')) || [];
//     const existingProductIndex = cart.findIndex(product => product.id === productId);

//     if (existingProductIndex > -1) {
//         cart[existingProductIndex].quantity += quantity;
//     } else {
//         cart.push({ id: productId, price: price, imageUrl: imageUrl, quantity: quantity });
//     }

//     localStorage.setItem('cart', JSON.stringify(cart));
//     alert('Producto añadido al carrito');
// }



// Modificamos el metodo para que tome en cuenta el stock disponible y no permita agregar más productos de los existentes en el stock, tambien maneja una función addtocart para el boton añadir al carrito, tambien se agrega una función loadCart para manejar la adición al carrito de compras y que los productos migren a la página del render del carrito, esto se logra porque loadCart hace que se carguen desde la función localStorage y se muestren en el carritopor tanto actualiza el localStorage cuando se añade un nuevo producto, se agregan mensajes de consola para  identificar futuros errores --- Para evitar que el carrito sume más productos de los existentes en stock crear una variable en el almacenamiento local (localStorage) para cada producto en el carrito, que rastree la cantidad actual de ese producto. Cuando el usuario intenta agregar más de ese producto desde la tienda, primero debemos verificar la cantidad existente en el carrito y asegurarnos de que no se supere el stock disponible. --- Asegurarnos de que el mensaje de alerta de "Producto añadido al carrito" no se muestre si no se ha añadido efectivamente ningún producto debido a las restricciones de stock para esto crearemos una nueva variable productAdded. Manejo de productAdded: Se ha agregado una variable productAdded que se inicializa como false. Esta variable se establece en true solo si realmente se añade un producto al carrito. Esto garantiza que el mensaje "Producto añadido al carrito" se muestre únicamente cuando el producto se añade efectivamente..

// shop-shoppingcart.js
// Método para manejar el incremento y decremento de productos, asegurándose de no exceder el stock disponible
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
            alert('No puedes añadir más productos que el carrito que el stock disponible');
            existingProduct.quantity = stock;  // Set to max stock if over
        } else {
            existingProduct.quantity = newQuantity;
            productAdded = true;
        }
    } else {
        if (quantity > stock) {
            alert('No puedes añadir más productos que el stock disponible');
            // Si esta linea se comenta o elimina se convierte en un codigo mas riguroso y no permite adicionar al usuario la cantidad maxima de producto disponnible en caso de que la selección sea mayor al producto en stock ---- Pero si la linea se usa el usuario se permite agregar al usuario los productos psaltando la alerta que no se puede agreggar mas productos que los disponibbles pero en el carrito aparecera solo el maximo que esta disponible en stock para comprar
            // cart.push({ id: productId, price: price, imageUrl: imageUrl, quantity: stock });
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
function loadCart() {
    console.log("loadCart called");
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    console.log("Cart contents:", cart);
    const cartItemsContainer = document.querySelector('.cart-items');
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

        productElement.innerHTML = `
            <img src="${product.imageUrl}" alt="Imagen del producto">
            <div class="cart-item-details">
                <h3>Producto ID: ${product.id}</h3>
                <p>Precio: $${product.price}</p>
                <p>Cantidad: ${product.quantity}</p>
                <p>Total: $${productTotalPrice.toFixed(2)}</p>
            </div>
        `;

        cartItemsContainer.appendChild(productElement);
    });

    cartItemCount.textContent = totalItems;
    totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
}

// Call loadCart when the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOMContentLoaded event fired");
    loadCart();
});