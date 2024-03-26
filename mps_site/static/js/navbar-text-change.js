const tcvText = document.getElementById("tcv-text");
const joinText = document.getElementById("join-text");

// Function to update text content based on media query
function updateTextContent() {
    if (window.matchMedia("(max-width: 600px)").matches) {
        tcvText.textContent = "TCV";
        joinText.textContent = "JOIN";
    } else {
        tcvText.textContent = "The College View";
        joinText.textContent = "JOIN US";
    }
}

// Initial call to update text content
updateTextContent();

// Listen for window resize events to update text content
window.addEventListener("resize", updateTextContent);