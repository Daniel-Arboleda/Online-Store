// game.js

// Función para seleccionar la carta en el DOM y que el label cambie de estado
function toggleCardSelection(cardContainer) {
    const label = cardContainer.querySelector('.card-label');
    if (label) {
        label.textContent = label.textContent === "Head" ? "Select" : "Head";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    let balance = 1000;
    let jackpot = 5000;

    document.getElementById("balance").innerText = balance;
    document.getElementById("jackpot").innerText = jackpot;

    const suits = ["Hearts", "Diamonds", "Clubs", "Spades"];
    const ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"];
    const cards = document.querySelectorAll(".card");
    const dealButton = document.getElementById("deal-button");
    const betButton = document.getElementById("bet-button");

    // Función para obtener la ruta de la imagen de la carta
    function getCardImagePath(rank, suit) {
        return `Pokeran/static/img/cards/${rank}_of_${suit}.png`;
    }

    function validatePlayerHand(data) {
  if (!Array.isArray(data.player_hand)) return false;

  return data.player_hand.every(card =>
    card.hasOwnProperty('rank') &&
    card.hasOwnProperty('suit') &&
    card.hasOwnProperty('image_filename')
  );
}

fetch('/api/get-player-hand')
  .then(response => response.json())
  .then(data => {
    if (validatePlayerHand(data)) {
      const balance = parseInt(data.balance, 10);
      const jackpot = parseInt(data.jackpot, 10);
      // Procesa los datos de las cartas y realiza operaciones numéricas
      console.log('Balance:', balance);
      console.log('Jackpot:', jackpot);
    } else {
      console.error('Estructura JSON inconsistente');
    }
  })
  .catch(error => console.error('Error en la comunicación con el servidor', error));


    // Función para mostrar una carta en el DOM
    function displayCard(rank, suit, elementId) {
        const imgPath = getCardImagePath(rank, suit);
        const cardElement = document.getElementById(elementId);
        // cardElement.innerHTML = `<img src="${imgPath}" alt="${rank} of ${suit}">`;
        // Asegurarse de que la imagen se carga correctamente en el DOM
        const img = document.createElement("img");
        img.src = imgPath;
        img.alt = `${rank} of ${suit}`;
        cardElement.innerHTML = ""; // Limpiar contenido anterior
        cardElement.appendChild(img); // Insertar nueva imagen
    }

    // Repartir cartas haciendo una llamada AJAX
    async function dealCards() {
        try {
            const response = await fetch('/deal-new-hand/'); // Corrige la URL aquí
            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.status}`);
            }
            const data = await response.json();
            if (!data || !Array.isArray(data.hand) || data.hand.length === 0) {
                throw new Error('Datos no válidos: La respuesta no contiene cartas válidas');
            }
            renderCards(data.hand);
        } catch (error) {
            console.error('Error al repartir las cartas:', error);
            alert(`Ocurrió un error: ${error.message}`);
        }
    }
    
    // async function dealCards() {
    //     try {
    //       const response = await fetch('url-del-servidor/api/deal-cards');
      
    //       // Verifica si la respuesta del servidor es exitosa (código 200).
    //       if (!response.ok) {
    //         throw new Error(`Error en la solicitud: ${response.status}`);
    //       }
      
    //       const data = await response.json();
      
    //       // Valida que el JSON contenga los datos esperados (por ejemplo, cartas).
    //       if (!data || !Array.isArray(data.cards) || data.cards.length === 0) {
    //         throw new Error('Datos no válidos: La respuesta no contiene cartas válidas');
    //       }
      
    //       // Procesa los datos si son válidos.
    //       renderCards(data.cards);
    //     } catch (error) {
    //       console.error('Error al repartir las cartas:', error);
    //       alert(`Ocurrió un error: ${error.message}`);
    //     }
    //   }
      
    function renderCards(cards) {
        // Lógica para mostrar las cartas en la interfaz
        const cardContainer = document.getElementById('card-container'); // Asegúrate de que tienes un contenedor para las cartas
    
        cardContainer.innerHTML = ''; // Limpiar cartas previas
    
        // Mostrar cartas boca abajo
        for (let i = 0; i < cards.length; i++) {
            const cardElement = document.createElement('div');
            cardElement.classList.add('card');
            cardElement.innerHTML = '<img src="static/img/cards/back_of_card.png" alt="Card Back">'; // Ruta a la carta boca abajo
            cardContainer.appendChild(cardElement);
        }
    
        // Después de un tiempo, mostrar las cartas reales
        setTimeout(() => {
            for (let i = 0; i < cards.length; i++) {
                displayCard(cards[i].rank, cards[i].suit, `card-${i}`);
            }
        }, 1000); // Mostrar cartas reales después de 1 segundo (ajusta el tiempo según lo desees)
    }
      
    function revealCards(cards) {
        const cardContainer = document.getElementById('card-container');
    
        cards.forEach((card, index) => {
            const cardElement = cardContainer.children[index]; // Obtener la carta correspondiente
            cardElement.innerHTML = `<img src="{% static 'img/cards/' %}${card.rank}_of_${card.suit}.png" alt="${card.rank} of ${card.suit}">`;
        });
    }
    

    // Evento para repartir cartas al hacer clic en el botón "Deal"
    dealButton.addEventListener("click", () => {
        if (balance > 0) {
            dealCards();
        } else {
            alert("No tienes suficiente balance para jugar.");
        }
    });

    // Evento para apostar al hacer clic en el botón "Bet"
    betButton.addEventListener("click", () => {
        if (balance >= 10) {
            balance -= 10;
            document.getElementById("balance").innerText = balance;
        } else {
            alert("Balance insuficiente para apostar.");
        }
    });
});

// Función para actualizar los premios
function updatePrizes(winningHand, coinsBet) {
    const prizeMultipliers = {
        "Escalera real": [250, 500, 750, 1000, 4000],
        "Cuatro doses": [200, 400, 600, 800, 1000],
        "Escalera real con comodines": [25, 50, 75, 100, 125],
        "Repoker": [15, 30, 45, 60, 75],
        "Escalera de color": [9, 18, 27, 36, 45],
        "Poker": [4, 8, 12, 16, 20],
        "Full": [4, 8, 12, 16, 20],
        "Color": [3, 6, 9, 12, 15],
        "Escalera": [2, 4, 6, 8, 10],
        "Trío": [1, 2, 3, 4, 5]
    };

    const prizes = prizeMultipliers[winningHand];
    if (prizes) {
        for (let i = 0; i < prizes.length; i++) {
            const prizeCell = document.querySelector(`.prize-${i + 1}`);
            prizeCell.innerText = prizes[i] * coinsBet; // Multiplica el premio por la cantidad de monedas apostadas
        }
    }
}
