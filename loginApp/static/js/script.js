document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector('.sidebar');
    const toggle = document.querySelector(".toggle");
    const searchBtn = document.querySelector(".search-box");
    const userImage = document.querySelector("#userImage"); 

    if (!sidebar || !toggle) {
        console.error("Sidebar or toggle element is missing!");
        return;
    }

    // Toggle the sidebar collapse
    toggle.addEventListener("click", () => {
        console.log("Toggle clicked!");
        sidebar.classList.toggle("close"); // This will add or remove the "close" class to collapse/expand sidebar
        const message = sidebar.classList.contains("close")
            ? "Sidebar collapsed!"
            : "Sidebar expanded!";
        // showToast(message); // Optionally display a toast message
    });


    // Open sidebar on search box click
    if (searchBtn) {
        searchBtn.addEventListener("click", () => {
            console.log("Search box clicked!");
            sidebar.classList.remove("close");
        });
    } else {
        console.warn("Search box not found!");
    }

    // Navigate to the profile page on user image click
    if (userImage) {
        userImage.addEventListener("click", () => {
            console.log("User image clicked!");
            window.location.href = "profile";
        });
    } else {
        console.warn("User image element not found!");
    }

    // Function to show a toast message
    function showToast(message) {
        console.log("Showing toast:", message); // Debug toast messages
        const toast = document.createElement("div");
        toast.innerText = message;
        toast.style.position = "fixed";
        toast.style.bottom = "20px";
        toast.style.right = "20px";
        toast.style.backgroundColor = "#333";
        toast.style.color = "#fff";
        toast.style.padding = "10px 20px";
        toast.style.borderRadius = "5px";
        toast.style.boxShadow = "0 0 10px rgba(0, 0, 0, 0.5)";
        toast.style.zIndex = "1000";
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    
});
