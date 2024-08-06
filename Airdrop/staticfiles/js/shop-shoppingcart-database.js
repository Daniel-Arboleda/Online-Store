// Agregar al carrito y guardar en la base de datos
async function addToCart(userId, productId, price, imageUrl, quantity) {
    const response = await fetch('/api/cart', {
        method: 'POST',
        body: JSON.stringify({ userId, productId, price, imageUrl, quantity }),
        headers: { 'Content-Type': 'application/json' }
    });

    if (response.ok) {
        const cart = await response.json();
        // Actualizar la interfaz con el nuevo carrito
    } else {
        alert('Error al agregar al carrito');
    }
}

// Cargar carrito desde la base de datos
async function loadCart(userId) {
    const response = await fetch(`/api/cart?userId=${userId}`);
    if (response.ok) {
        const cart = await response.json();
        // Renderizar carrito en la página
    } else {
        alert('Error al cargar el carrito');
    }
}
