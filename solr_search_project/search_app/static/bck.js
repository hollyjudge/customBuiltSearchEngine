// Get the button element
const button = document.getElementById('searchButton');

// Add an event listener to the button to change the background color
button.addEventListener('click', function() {
  document.body.classList.toggle('background1');
});

const toggleButton = document.getElementById('filterButton');
const sidebar = document.querySelector('.sidebar');

toggleButton.addEventListener('click', function() {
  sidebar.classList.toggle('hidden');
});

