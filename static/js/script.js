const locationInput = document.getElementById('location');
const suggestionsList = document.createElement('ul');
suggestionsList.classList.add('list-group', 'mt-2');
locationInput.parentNode.appendChild(suggestionsList);

locationInput.addEventListener('input', function () {
    const query = locationInput.value;

    if (query.length > 1) {
        fetch(`/location-autocomplete/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = '';
                data.suggestions.forEach(suggestion => {
                    const listItem = document.createElement('li');
                    listItem.textContent = suggestion;
                    listItem.classList.add('list-group-item');
                    listItem.addEventListener('click', () => {
                        locationInput.value = suggestion;
                        suggestionsList.innerHTML = '';
                    });
                    suggestionsList.appendChild(listItem);
                });
            });
    } else {
        suggestionsList.innerHTML = '';
    }
});