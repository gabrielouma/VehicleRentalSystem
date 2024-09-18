// Select all filter buttons and filterable cards
const filterButtons = document.querySelectorAll(".fiter_buttons button");
const filterableCards = document.querySelectorAll(".filterable_cards .card");

// Define the filterCards function
const filterCards = e => {
    // Find the currently active button
    const currentActiveButton = document.querySelector(".fiter_buttons .active");
    
    // Remove the active class from it
    if (currentActiveButton) {
        currentActiveButton.classList.remove("active");
    }
    e.target.classList.add("active");
    
    // Iterate over each filterable card
    filterableCards.forEach(card => {
        card.classList.add("hide");
        if(card.dataset.name === e.target.dataset.name || e.target.dataset.name === "all"){
        card.classList.remove("hide");
        }
    });
};

// Add click event listerner to each filter button
filterButtons.forEach(button => button.addEventListener("click", filterCards));

// =================================================================================

// =================================================================================
function searchbox() {
    const input = document.getElementById('mysearch').value.toLowerCase();
    const cards = document.querySelectorAll('.filterable_cards .card');
    var notfound = document.getElementById("notfound");
    let nomatch = true;
    
    // Loop through the cards and display only those that match the search input
    cards.forEach(card => {
        const location = card.querySelector('.location').textContent.toLowerCase();
        
        if (location.includes(input)) {
            card.style.display = ''; // Show the card if it matches
            nomatch = false;
        } else {
            card.style.display = 'none'; // Hide the card if it doesn't match
        }
    });

    if(nomatch){
        notfound.style.display = 'block';
    }else{
        notfound.style.display = 'none';
    }
}