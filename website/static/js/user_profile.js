document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const cardsContainer = document.getElementById('cards-container');
    const cards = cardsContainer.getElementsByClassName('card');
  
    searchInput.addEventListener('input', () => {
      const filter = searchInput.value.toLowerCase();
      
      Array.from(cards).forEach(card => {
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        
        if (title.includes(filter)) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });