/**
 * @fileoverview Task Manager - Snackbar Component
 * Handles displaying notifications using Material Design 3 snackbars
 */

// Store a reference to the snackbar instance
let snackbarInstance = null;

/**
 * Initialize the snackbar component
 * @return {?Object} The MDCSnackbar instance
 */
function initializeSnackbar() {
  // Use the global instance if available
  if (window.taskManagerSnackbar) {
    snackbarInstance = window.taskManagerSnackbar;
    return snackbarInstance;
  }

  const snackbarElement = document.getElementById('message-snackbar');
  if (!snackbarElement) {
    console.error('Snackbar element not found');
    return null;
  }

  // Create the instance if it doesn't exist
  if (!snackbarInstance) {
    try {
      snackbarInstance = new window.mdc.snackbar.MDCSnackbar(snackbarElement);
      snackbarInstance.closeOnEscape = true;
      console.log('Snackbar initialized successfully');
    } catch (error) {
      console.error('Error initializing snackbar:', error);
      return null;
    }
  }

  return snackbarInstance;
}

/**
 * Show a message in the snackbar
 * @param {string} message The message to display
 * @param {string=} type The message type: 'success', 'warning', or 'error'
 * @param {number=} duration Duration in milliseconds to show the message
 */
function showMessage(message, type = 'success', duration = 5000) {
  const snackbarElement = document.getElementById('message-snackbar');
  if (!snackbarElement) return;

  // Try to use the global instance first, then the module instance, or create a new one
  const mdcSnackbar = window.taskManagerSnackbar || snackbarInstance || initializeSnackbar();
  if (!mdcSnackbar) {
    console.error('Failed to initialize snackbar');
    return;
  }

  // Set message text
  mdcSnackbar.labelText = message;

  // Set duration
  mdcSnackbar.timeoutMs = duration;

  // Set appropriate class for styling
  snackbarElement.classList.remove(
      'mdc-snackbar--success',
      'mdc-snackbar--warning',
      'mdc-snackbar--error',
      'mdc-snackbar--info'
  );
  snackbarElement.classList.add(`mdc-snackbar--${type}`);

  console.log('Showing snackbar message:', message, 'Type:', type);

  // Show the snackbar
  mdcSnackbar.open();
}

/**
 * Show a success message
 * @param {string} message The message to display
 * @param {number=} duration Duration in milliseconds to show the message
 */
function showSuccess(message, duration = 5000) {
  showMessage(message, 'success', duration);
}

/**
 * Show a warning message
 * @param {string} message The message to display
 * @param {number=} duration Duration in milliseconds to show the message
 */
function showWarning(message, duration = 7000) {
  showMessage(message, 'warning', duration);
}

/**
 * Show an error message
 * @param {string} message The message to display
 * @param {number=} duration Duration in milliseconds to show the message
 */
function showError(message, duration = 10000) {
  showMessage(message, 'error', duration);
}

/**
 * Process Django messages and display them as snackbars
 */
function processDjangoMessages() {
  // Find message container
  const messageContainer = document.querySelector('.message-fallback-container');
  if (!messageContainer) return;

  // Get all messages
  const messages = messageContainer.querySelectorAll('.message-fallback');
  if (!messages.length) return;

  // Process each message
  messages.forEach((message, index) => {
    const messageText = message.dataset.message || message.textContent;

    // Determine message type
    let messageType = 'success';
    if (message.classList.contains('error')) {
      messageType = 'error';
    } else if (message.classList.contains('warning')) {
      messageType = 'warning';
    } else if (message.classList.contains('info')) {
      messageType = 'info';
    }

    console.log('Processing message:', messageText, 'Type:', messageType);

    // Show the message with a delay for multiple messages
    setTimeout(() => {
      showMessage(messageText, messageType);
    }, index * 300); // Stagger messages slightly if there are multiple
  });
}

// Initialization is now handled in main.js

// Export for use in other modules
export {
  initializeSnackbar,
  showMessage,
  showSuccess,
  showWarning,
  showError,
  processDjangoMessages
};
