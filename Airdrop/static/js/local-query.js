// Una solución común para este tipo de requerimiento implica el uso de almacenamiento local del navegador o cookies, dependiendo de las necesidades específicas de persistencia y acceso a los datos

//  Guardar el saldo en el almacenamiento local

document.addEventListener('DOMContentLoaded', function() {
    const recargarSaldoBtn = document.getElementById('recargarSaldoBtn');
    recargarSaldoBtn.addEventListener('click', function() {
        // Simula la actualización del saldo, por ejemplo, después de una transacción
        const nuevoSaldo = '$1,050'; // Supongamos que este valor viene de alguna operación
        const saldoAmountElement = document.querySelector('.saldo-amount');
        saldoAmountElement.textContent = nuevoSaldo;
        
        // Guardar el saldo actualizado en el almacenamiento local
        localStorage.setItem('saldo', nuevoSaldo);
    });
});



// Leer el saldo desde el almacenamiento local

document.addEventListener('DOMContentLoaded', function() {
    const recargarSaldoBtn = document.getElementById('recargarSaldoBtn');
    recargarSaldoBtn.addEventListener('click', function() {
        // Simula la actualización del saldo, por ejemplo, después de una transacción
        const nuevoSaldo = '$1,050'; // Supongamos que este valor viene de alguna operación
        const saldoAmountElement = document.querySelector('.saldo-amount');
        saldoAmountElement.textContent = nuevoSaldo;
        
        // Guardar el saldo actualizado en el almacenamiento local
        localStorage.setItem('saldo', nuevoSaldo);
    });
});
