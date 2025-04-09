/**
 * Direct form storage implementation - no modules, no imports, just plain JavaScript
 */
window.addEventListener('DOMContentLoaded', function() {
  console.log('Direct form storage script loaded');
  
  // Find the assignment form
  const form = document.getElementById('assignment-form');
  if (!form) {
    console.log('No assignment form found');
    return;
  }
  
  // Define the fields to store
  const fieldConfig = {
    'id_due_date': 'assignment_due_date',
    'id_name': 'assignment_name',
    'id_description': 'assignment_description',
    'id_status': 'assignment_status'
  };
  
  // Check if this is a form with validation errors
  // Look for any error messages or error classes on form elements
  const hasErrors = form.querySelector('.errorlist') !== null || 
                   form.querySelector('.has-error') !== null ||
                   form.querySelector('.error') !== null;
  
  console.log('Form has validation errors:', hasErrors);
  
  // If this is a new form with no errors, clear any stored data
  if (!hasErrors) {
    Object.values(fieldConfig).forEach(function(key) {
      localStorage.removeItem(key);
    });
    console.log('New form detected, cleared localStorage');
    return;
  }
  
  // If we have validation errors, set up storage and restore values
  Object.entries(fieldConfig).forEach(function([fieldId, storageKey]) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    // Store field data in localStorage when it changes
    field.addEventListener('change', function() {
      localStorage.setItem(storageKey, this.value);
      console.log('Stored value for', fieldId, ':', this.value);
    });
    
    // Restore from localStorage if we have a saved value
    if (localStorage.getItem(storageKey)) {
      field.value = localStorage.getItem(storageKey);
      console.log('Restored value for', fieldId, ':', field.value);
    }
  });
  
  // Clear localStorage on successful form submission
  form.addEventListener('submit', function() {
    // Only clear if the form is valid
    if (form.checkValidity()) {
      Object.values(fieldConfig).forEach(function(key) {
        localStorage.removeItem(key);
      });
      console.log('Form submitted successfully, cleared localStorage');
    }
  });
});
