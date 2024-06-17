// // Selecciona el botón "Abrir cuenta" por su id
// const openAccountBtn = document.getElementById('open_account');

// // Define la función que se activará al hacer clic en el botón
// function openAccountPopup() {
//     // Obtiene la URL de la página "open-account" del atributo de datos
//     const openAccountURL = openAccountBtn.dataset.openAccountUrl;
    
//     // Abre una nueva ventana emergente con la página "open-account"
//     window.open(openAccountURL, '_blank', 'width=600,height=400');
// }

// // Agrega un evento de clic al botón "Abrir cuenta" que llame a la función openAccountPopup
// openAccountBtn.addEventListener('click', openAccountPopup);


// ---------------------------------------------------------------


// // Selecciona el botón "Abrir cuenta" por su id
// document.addEventListener('DOMContentLoaded', function() {
//     const loginAccountBtn = document.getElementById('login-account');
//     const btnLogin = document.getElementById('btn-login');

//     if (loginAccountBtn) {
//         loginAccountBtn.addEventListener('click', function() {
//             const loginURL = loginAccountBtn.dataset.loginUrl;
//             window.open(loginURL, '_blank', 'width=600,height=400');
//         });
//     }

//     if (btnLogin) {
//         btnLogin.addEventListener('click', function(event) {
//             if (event.target == segundaVentanaModal) {
//                 closeWindow();
//             }
//         // Event listener para cerrar la segunda ventana emergente cuando se hace clic fuera de ella
//         window.addEventListener("click", function() {
            
//         });
//             // Asumiendo que quieres redirigir a 'home' directamente sin usar el href del enlace inexistente
//             window.location.href = "{% url 'home' %}"; // Utiliza la sintaxis de Django para inyectar la URL directamente
//         });
//     }
// });

// ---------------------------------------------------------------


// ---------------------------------------------------------------


// Codigo de la segunda ventana emergente




// document.addEventListener("DOMContentLoaded", function() {
//     var openSecondModalButton = document.getElementById("openSecondModalButton");
//     var segundaVentanaModal = document.getElementById("modal-segunda-ventana");
//     var closeButtonSegunda = document.querySelector("#modal-segunda-ventana .close");

//     // Función para mostrar la segunda ventana emergente
//     function showSecondModal() {
//         segundaVentanaModal.style.display = "block";
//     }

//     // Función para cerrar la segunda ventana emergente
//     function closeSecondModal() {
//         segundaVentanaModal.style.display = "none";
//     }

//     // Event listener para abrir la segunda ventana emergente cuando se hace clic en el botón "+"
//     openSecondModalButton.addEventListener("click", showSecondModal);

//     // Event listener para cerrar la segunda ventana emergente cuando se hace clic en el botón de cierre
//     closeButtonSegunda.addEventListener("click", closeSecondModal);

//     // Event listener para cerrar la segunda ventana emergente cuando se hace clic fuera de ella
//     window.addEventListener("click", function(event) {
//         if (event.target == segundaVentanaModal) {
//             closeSecondModal();
//         }
//     });
// });


// ---------------------------------------------------------------




// --------------------------------------------------------------



// ---------------------------------------------------------------


// // theme-toggle.js
// document.addEventListener('DOMContentLoaded', function() {
//     // Asegúrate de que el ID aquí coincide con el ID en tu HTML
//     const themeToggle = document.getElementById('theme-toggle');

//     themeToggle.addEventListener('click', function() {
//         document.body.classList.toggle('dark_theme');
//     });
// });


// ---------------------------------------------------------------



// JavaScript para el despliege de los contenedores

function toggleVisibility(header) {
    var content = header.nextElementSibling; // Obtiene el elemento hermano directo, que es el contenido desplegable
    if (content.style.display === "block") {
        content.style.display = "none"; // Oculta el contenido
    } else {
        content.style.display = "block"; // Muestra el contenido
        content.style.overflow = "hidden"; // Asegura que todo el contenido esté dentro del contenedor
    }
}

