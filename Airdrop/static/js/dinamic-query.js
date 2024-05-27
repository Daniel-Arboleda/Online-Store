// El enfoque más seguro es que la página realice una solicitud al servidor para obtener el saldo actualizado cada vez que el usuario accede a ella o después de cualquier transacción que pueda alterar el saldo. Esto se puede hacer mediante

// Ejemplo de JavaScript (usando Fetch API):
document.addEventListener('DOMContentLoaded', function() {
    fetch('{% url "api_get_saldo" %}')
    .then(response => response.json())
    .then(data => {
        const saldoBoxP = document.querySelector('.saldo-box p');
        saldoBoxP.textContent = `$${data.saldo}`;
    })
    .catch(error => console.error('Error al cargar el saldo:', error));
});



// Django View:
// from django.http import JsonResponse

// def get_saldo(request):
//     # Asume que tienes un método para obtener el saldo del usuario
//     saldo = request.user.get_saldo()
//     return JsonResponse({'saldo': saldo})
