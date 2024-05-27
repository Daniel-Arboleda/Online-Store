document.addEventListener('DOMContentLoaded', function() {
    const accountForm = document.getElementById('account-form');
    const btnAccount = document.getElementById('btn-account');

    accountForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Previene el envío normal del formulario

        // Asegura que el formulario se envíe programáticamente
        fetch(accountForm.action, {
            method: 'POST',
            body: new FormData(accountForm)
        }).then(response => {
            if (response.ok) {
                // Redirige solo después de una respuesta exitosa
                window.location.href = btnAccount.getAttribute('data-url');
            } else {
                response.text().then(text => console.error('Error en la respuesta del servidor:', text));

            }
        }).catch(error => console.error('Error:', error));
    });
});

