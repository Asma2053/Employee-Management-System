function fetchSuggestions() {
    const nameInput = document.getElementById("name");
    const suggestionsBox = document.getElementById("suggestions");

    const query = nameInput.value.trim();

    if (query.length > 0) {
        fetch(`/get_user_suggestions/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = "";
                if (data.suggestions && data.suggestions.length > 0) {
                    data.suggestions.forEach(user => {
                        const suggestion = document.createElement("div");
                        suggestion.textContent = user;
                        suggestion.style.cursor = "pointer";
                        suggestion.addEventListener("click", function () {
                            nameInput.value = user;  // Store selected name
                            suggestionsBox.innerHTML = "";  // Clear suggestions
                        });
                        suggestionsBox.appendChild(suggestion);
                    });
                } else {
                    suggestionsBox.innerHTML = "<p>No results found</p>";
                }
            })
            .catch(error => {
                console.error("Error fetching user suggestions:", error);
            });
    } else {
        suggestionsBox.innerHTML = "";  // Clear suggestions if input is empty
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const nameInput = document.getElementById("name");
    nameInput.addEventListener("input", fetchSuggestions); // Trigger on input event
});
