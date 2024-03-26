let animationEnabled = false;
let clickCount = 0;

function toggleTransformation() {
    const element = document.getElementById('webmaster-element');
    clickCount++;
    
    if (clickCount === 6) {
        element.style.animation = 'none'; // Stop the animation
        clickCount = 0; // Reset click count
    } else if (clickCount === 5) {
        const audio = document.getElementById('clickSound');
        audio.play(); // Play the sound
        element.style.animation = 'rotateAnimation 1s linear infinite'; // Resume the animation
        animationEnabled = true; // Set animation state to true
    } else {
        if (animationEnabled) {
            element.style.animation = 'none'; // Pause the animation
        } else {
            element.style.animation = 'rotateAnimation 1s linear infinite'; // Resume the animation
            animationEnabled = true; // Set animation state to true
        }
    }
}