/**
 * Simple direct snackbar implementation to ensure messages are displayed
 */
document.addEventListener('DOMContentLoaded', function() {
  // Find the snackbar element
  const snackbarElement = document.getElementById('message-snackbar');
  if (!snackbarElement) return;

  // Initialize the snackbar
  const snackbar = mdc.snackbar.MDCSnackbar.attachTo(snackbarElement);
  
  // Find message container
  const messageContainer = document.querySelector('.message-fallback-container');
  if (!messageContainer) return;
  
  // Get all messages
  const messages = messageContainer.querySelectorAll('.message-fallback');
  if (!messages.length) return;
  
  console.log('Found', messages.length, 'messages to display');
  
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
    }, index * 300); // Stagger messages slightly if there are multiple
  });
});
