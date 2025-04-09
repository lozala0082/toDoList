/**
 * Task Manager - Initialization Script
 * Extracted from base.html inline scripts
 */

// Auto-init all components
window.mdc.autoInit();

// Initialize common MDC components
document.addEventListener('DOMContentLoaded', function() {
    // Add ripples to buttons
    document.querySelectorAll(".mdc-button").forEach((button) => {
        if (button) mdc.ripple.MDCRipple.attachTo(button);
    });

    // Add ripples to icon buttons
    document.querySelectorAll(".mdc-icon-button").forEach((button) => {
        if (button) {
            const ripple = mdc.ripple.MDCRipple.attachTo(button);
            ripple.isUnbounded = true; // Important for icon buttons
        }
    });

    // Initialize top app bar
    const topAppBarElement = document.querySelector('.mdc-top-app-bar');
    if (topAppBarElement) {
        mdc.topAppBar.MDCTopAppBar.attachTo(topAppBarElement);
    }

    // Initialize snackbar
    const snackbarElement = document.querySelector('.mdc-snackbar');
    if (snackbarElement) {
        const snackbar = mdc.snackbar.MDCSnackbar.attachTo(snackbarElement);

        // Configure snackbar
        snackbar.timeoutMs = 5000; // Show for 5 seconds
        snackbar.closeOnEscape = true; // Allow closing with Escape key

        // Show messages in snackbar if any
        const fallbackMessages = document.querySelectorAll('.message-fallback');
        if (fallbackMessages.length > 0) {
            // Get the first message
            const firstMessage = fallbackMessages[0];
            const messageText = firstMessage.textContent.trim();
            const messageType = firstMessage.classList.contains('success') ? 'success' :
                              firstMessage.classList.contains('error') ? 'error' :
                              firstMessage.classList.contains('warning') ? 'warning' :
                              firstMessage.classList.contains('info') ? 'info' : '';

            // Set snackbar label text
            snackbarElement.querySelector('.mdc-snackbar__label').textContent = messageText;

            // Add appropriate class based on message type
            snackbarElement.classList.remove('success', 'error', 'warning', 'info');
            if (messageType) {
                snackbarElement.classList.add(messageType);
            }

            // Show the snackbar
            snackbar.open();
        }
    }
});
