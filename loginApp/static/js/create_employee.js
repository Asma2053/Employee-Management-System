// Define the function before attaching event listeners
function fetchSuggestions() {
    const nameInput = document.getElementById("name");
    const suggestionsBox = document.getElementById("suggestions");

    const query = nameInput.value.trim();

    if (query.length > 0) {
        fetch(`/get_user_suggestions/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = "";
                if (data.suggestions && data.suggestions.length > 0) {  // Ensure 'suggestions' exists in the response
                    data.suggestions.forEach(user => {
                        const suggestion = document.createElement("div");
                        suggestion.textContent = user;  // Directly use 'user' since it's a string
                        suggestion.style.cursor = "pointer";
                        suggestion.addEventListener("click", function () {
                            nameInput.value = user;  // Use 'user' as it's a string now
                            suggestionsBox.innerHTML = "";  // Clear suggestions after selection
                        });
                        suggestionsBox.appendChild(suggestion);
                    });
                } else {
                    console.log("No results found"); // Debugging
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
    const suggestionsBox = document.getElementById("suggestions");

    nameInput.addEventListener("input", fetchSuggestions);  // Use input event instead of keyup
});
