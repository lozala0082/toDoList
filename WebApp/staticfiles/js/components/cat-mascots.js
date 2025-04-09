/**
 * Task Manager - Cat Mascots Component
 * Handles interactions with the cat mascot elements
 */

// Motivational messages for the Lockedin Cat
const lockedinCatMessages = [
    "You're doing purrfect work today!",
    "Stay pawsitive, you've got this!",
    "Feline good about your progress!",
    "You're the cat's meow! Keep it up!",
    "Meowvelous job on your tasks!",
    "Stay focused and you'll be feline fine!",
    "Don't paws now, you're on a roll!",
    "You're making hiss-tory with your productivity!",
    "Claw your way to success, one task at a time!",
    "You're litter-ally crushing these assignments!"
];

// Hurry-up messages for the Bosscat
const bosscatMessages = [
    "Hurry up, I don't have nine lives to wait!",
    "Are you kitten me? Log in already!",
    "Stop procrastinating, it's meow or never!",
    "I'm not feline patient today, let's go!",
    "Paws what you're doing and get to work!",
    "Don't make me hiss at you, log in now!",
    "You're testing all of my nine lives with this delay!",
    "Less purr-crastination, more action!",
    "I'm the boss around here, chop chop!",
    "This isn't nap time, let's get moving!"
];

/**
 * Initialize cat mascot functionality
 */
function initializeCatMascots() {
    // Find all cat mascots
    const catMascots = document.querySelectorAll('.cat-mascot');

    catMascots.forEach(mascot => {
        // Create a message bubble element if it doesn't exist
        let messageBubble = mascot.querySelector('.cat-message-bubble');

        if (!messageBubble) {
            messageBubble = document.createElement('div');
            messageBubble.className = 'cat-message-bubble';
            messageBubble.style.display = 'none';
            mascot.appendChild(messageBubble);
        }

        // Add click event listener if not already added
        if (!mascot.hasAttribute('data-initialized')) {
            mascot.setAttribute('data-initialized', 'true');
            mascot.addEventListener('click', function() {
            // Determine which cat was clicked
            const catType = mascot.getAttribute('data-cat-type');
            let message = '';

            // Select a random message based on cat type
            if (catType === 'lockedin') {
                const randomIndex = Math.floor(Math.random() * lockedinCatMessages.length);
                message = lockedinCatMessages[randomIndex];
            } else if (catType === 'bosscat') {
                const randomIndex = Math.floor(Math.random() * bosscatMessages.length);
                message = bosscatMessages[randomIndex];
            }

            // Display the message
            messageBubble.textContent = message;
            messageBubble.style.display = 'block';

            // Add animation class
            messageBubble.classList.add('show-message');

            // Hide the message after a delay
            setTimeout(() => {
                messageBubble.classList.remove('show-message');
                setTimeout(() => {
                    messageBubble.style.display = 'none';
                }, 500); // Wait for fade out animation to complete
            }, 8000); // Show message for 8 seconds
            });
        }
    });
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', initializeCatMascots);

// Export for use in other modules
export { initializeCatMascots };
