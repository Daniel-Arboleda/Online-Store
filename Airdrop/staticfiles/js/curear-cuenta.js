document.addEventListener('DOMContentLoaded', function() {
    const accountForm = document.getElementById('account-form');
    const loginUrl = document.getElementById('open_account').href;

    accountForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Previene el envío normal del formulario
        
        // Asegura que el formulario se envíe programáticamente
        fetch(accountForm.action, {
            method: 'POST',
            body: new FormData(accountForm)
        })
        .then(response => {
            if (response.ok) {
                window.location.href = loginUrl; // Redirige solo después de una respuesta exitosa
            } else {
                console.error('Error en la respuesta del servidor');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});

