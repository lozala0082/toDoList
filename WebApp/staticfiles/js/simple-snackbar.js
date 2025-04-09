/**
 * Ultra-simple snackbar implementation with no dependencies
 * This script will directly handle displaying Django messages in a snackbar
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log('Simple snackbar script loaded');
  
  // Function to show a message in the snackbar
  function showSnackbar(message, type) {
    console.log('Attempting to show snackbar:', message, type);
    
    // Create snackbar element if it doesn't exist
    let snackbar = document.getElementById('simple-snackbar');
    if (!snackbar) {
      snackbar = document.createElement('div');
      snackbar.id = 'simple-snackbar';
      snackbar.style.position = 'fixed';
      snackbar.style.bottom = '20px';
      snackbar.style.left = '50%';
      snackbar.style.transform = 'translateX(-50%)';
      snackbar.style.minWidth = '250px';
      snackbar.style.padding = '16px 24px';
      snackbar.style.borderRadius = '4px';
      snackbar.style.boxShadow = '0 3px 5px rgba(0,0,0,0.2)';
      snackbar.style.color = 'white';
      snackbar.style.textAlign = 'center';
      snackbar.style.zIndex = '10000';
      snackbar.style.transition = 'opacity 0.3s, visibility 0.3s';
      snackbar.style.opacity = '0';
      snackbar.style.visibility = 'hidden';
      document.body.appendChild(snackbar);
    }
    
    // Set background color based on message type
    if (type === 'error') {
      snackbar.style.backgroundColor = '#f44336'; // Red
    } else if (type === 'warning') {
      snackbar.style.backgroundColor = '#ff9800'; // Orange
    } else if (type === 'info') {
      snackbar.style.backgroundColor = '#2196f3'; // Blue
    } else {
      snackbar.style.backgroundColor = '#4caf50'; // Green (success)
    }
    
    // Set message text
    snackbar.textContent = message;
    
    // Show the snackbar
    snackbar.style.opacity = '1';
    snackbar.style.visibility = 'visible';
    
    // Hide after 5 seconds (or 10 for errors)
    const duration = type === 'error' ? 10000 : 5000;
    setTimeout(function() {
      snackbar.style.opacity = '0';
      snackbar.style.visibility = 'hidden';
    }, duration);
  }
  
  // Process Django messages
  function processDjangoMessages() {
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
        showSnackbar(messageText, messageType);
      }, index * 500); // Stagger messages slightly if there are multiple
    });
  }
  
  // Process messages immediately
  processDjangoMessages();
});
