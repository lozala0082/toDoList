/**
 * Direct snackbar implementation - no modules, no imports, just plain JavaScript
 */
window.addEventListener('DOMContentLoaded', function() {
  console.log('Direct snackbar script loaded');
  
  // Wait a short moment to ensure everything is loaded
  setTimeout(function() {
    // Find the snackbar element
    const snackbarElement = document.getElementById('message-snackbar');
    if (!snackbarElement) {
      console.error('Snackbar element not found');
      return;
    }
    
    // Initialize the snackbar
    let snackbar;
    try {
      snackbar = new mdc.snackbar.MDCSnackbar(snackbarElement);
      console.log('Snackbar initialized successfully');
    } catch (error) {
      console.error('Error initializing snackbar:', error);
      return;
    }
    
    // Find message container
    const messageContainer = document.querySelector('.message-fallback-container');
    if (!messageContainer) {
      console.log('No message container found');
      return;
    }
    
    // Get all messages
    const messages = messageContainer.querySelectorAll('.message-fallback');
    if (!messages.length) {
      console.log('No messages found');
      return;
    }
    
    console.log('Found', messages.length, 'messages to display');
    
    // Process each message
    messages.forEach(function(message, index) {
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
      setTimeout(function() {
        // Set message text
        snackbar.labelText = messageText;
        
        // Set duration based on type
        snackbar.timeoutMs = messageType === 'error' ? 10000 : 5000;
        
        // Set appropriate class for styling
        snackbarElement.classList.remove(
          'mdc-snackbar--success', 
          'mdc-snackbar--warning', 
          'mdc-snackbar--error',
          'mdc-snackbar--info'
        );
        snackbarElement.classList.add(`mdc-snackbar--${messageType}`);
        
        // Show the snackbar
        snackbar.open();
        console.log('Opened snackbar with message:', messageText);
      }, index * 500); // Stagger messages slightly if there are multiple
    });
  }, 100); // Short delay to ensure everything is loaded
});
