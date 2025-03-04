const cards = []; // Array to hold card objects
let selectedCard = null;

// Function to fetch cards from Flask API
async function fetchCards() {
  try {
    const response = await fetch('/api/cards'); // Replace '/api/cards' with your actual endpoint
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    cards.length = 0; //clear existing cards
    data.forEach(cardData => {
      cards.push({
        ...cardData,
        element: createCardElement(cardData)
      });
    });
    displayCards();
  } catch (error) {
    console.error('Error fetching cards:', error);
  }
}

// Function to create a card element
function createCardElement(cardData) {
  const cardDiv = document.createElement('div');
  cardDiv.classList.add('card');
  cardDiv.id = cardData.id; // Assuming your card data has an 'id' field.
  cardDiv.textContent = cardData.value; // Example, replace with actual card data display
  cardDiv.addEventListener('click', () => selectCard(cardData.id));
  return cardDiv;
}

// Function to display cards on the page
function displayCards() {
  const cardContainer = document.getElementById('card-container'); //Assumes you have a div with this ID.
  cardContainer.innerHTML = ''; //clear existing cards
  cards.forEach(card => cardContainer.appendChild(card.element));
}

// Function to handle card selection
function selectCard(cardId) {
  if (selectedCard === cardId) {
    selectedCard = null;
    document.getElementById(cardId).classList.remove('selected');
  } else {
    if (selectedCard) {
      document.getElementById(selectedCard).classList.remove('selected');
    }
    selectedCard = cardId;
    document.getElementById(cardId).classList.add('selected');
  }
}

// Function to play a card (send data to Flask API)
async function playCard() {
  if (selectedCard) {
    try {
      const response = await fetch('/api/play', { // Replace '/api/play' with your actual endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cardId: selectedCard })
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Card played successfully:', data);
      // Update UI based on the response from the server
      fetchCards(); // Refresh cards after playing a card
    } catch (error) {
      console.error('Error playing card:', error);
    }
  }
}

// Add event listener for play button (assuming you have a button with id 'play-button')
document.getElementById('play-button').addEventListener('click', playCard);

// Initial fetch of cards on page load
fetchCards();

//Example of basic drawing (replace with your actual drawing logic)
const canvas = document.getElementById('myCanvas'); // Assumes you have a canvas with this ID.
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'red';
ctx.fillRect(10, 10, 50, 50);