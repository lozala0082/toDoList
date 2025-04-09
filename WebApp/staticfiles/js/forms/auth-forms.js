/**
 * Task Manager - Authentication Forms Handler
 * Handles login and registration forms
 */

import { initializeFormValidation, validatePassword, validatePasswordConfirmation } from '../utils/form-validation.js';
import { showError } from '../components/snackbar.js';

/**
 * Initialize the login form
 * @param {string} formId - The ID of the form element
 */
export function initializeLoginForm(formId = 'login-form') {
    const form = document.getElementById(formId);
    if (!form) return;

    // Initialize form validation
    initializeFormValidation(form);
    
    // Add form submission handler
    form.addEventListener('submit', handleLoginFormSubmit);
    
    // Initialize password visibility toggle
    initializePasswordVisibility(form);
}

/**
 * Initialize the registration form
 * @param {string} formId - The ID of the form element
 */
export function initializeRegistrationForm(formId = 'registration-form') {
    const form = document.getElementById(formId);
    if (!form) return;

    // Initialize form validation
    initializeFormValidation(form);
    
    // Add password confirmation validation
    const passwordField = form.querySelector('input[name="password1"]');
    const confirmField = form.querySelector('input[name="password2"]');
    
    if (passwordField && confirmField) {
        confirmField.addEventListener('blur', () => {
            validatePasswordConfirmation(confirmField, passwordField);
        });
        
        passwordField.addEventListener('change', () => {
            if (confirmField.value) {
                validatePasswordConfirmation(confirmField, passwordField);
            }
        });
    }
    
    // Add form submission handler
    form.addEventListener('submit', handleRegistrationFormSubmit);
    
    // Initialize password visibility toggle
    initializePasswordVisibility(form);
}

/**
 * Initialize password visibility toggle
 * @param {HTMLFormElement} form - The form element
 */
function initializePasswordVisibility(form) {
    const passwordFields = form.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(field => {
        // Create toggle button
        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.className = 'password-visibility-toggle material-symbols-outlined';
        toggleButton.textContent = 'visibility';
        toggleButton.setAttribute('aria-label', 'Toggle password visibility');
        
        // Add toggle button to field container
        const fieldContainer = field.closest('.mdc-text-field');
        if (fieldContainer) {
            // For outlined text fields
            const trailingContainer = fieldContainer.querySelector('.mdc-notched-outline__trailing');
            if (trailingContainer) {
                trailingContainer.appendChild(toggleButton);
            } else {
                // For filled text fields
                fieldContainer.appendChild(toggleButton);
            }
            
            // Add click event listener
            toggleButton.addEventListener('click', () => {
                // Toggle password visibility
                if (field.type === 'password') {
                    field.type = 'text';
                    toggleButton.textContent = 'visibility_off';
                } else {
                    field.type = 'password';
                    toggleButton.textContent = 'visibility';
                }
            });
        }
    });
}

/**
 * Handle login form submission
 * @param {Event} e - The submit event
 */
function handleLoginFormSubmit(e) {
    const form = e.target;
    
    // Get username and password fields
    const usernameField = form.querySelector('input[name="username"]');
    const passwordField = form.querySelector('input[name="password"]');
    
    // Basic validation
    if (!usernameField || !passwordField) return;
    
    if (!usernameField.value.trim()) {
        e.preventDefault();
        showError('Please enter your username');
        usernameField.focus();
        return;
    }
    
    if (!passwordField.value) {
        e.preventDefault();
        showError('Please enter your password');
        passwordField.focus();
        return;
    }
}

/**
 * Handle registration form submission
 * @param {Event} e - The submit event
 */
function handleRegistrationFormSubmit(e) {
    const form = e.target;
    
    // Get form fields
    const usernameField = form.querySelector('input[name="username"]');
    const passwordField = form.querySelector('input[name="password1"]');
    const confirmField = form.querySelector('input[name="password2"]');
    
    // Basic validation
    if (!usernameField || !passwordField || !confirmField) return;
    
    if (!usernameField.value.trim()) {
        e.preventDefault();
        showError('Please enter a username');
        usernameField.focus();
        return;
    }
    
    if (!passwordField.value) {
        e.preventDefault();
        showError('Please enter a password');
        passwordField.focus();
        return;
    }
    
    if (passwordField.value !== confirmField.value) {
        e.preventDefault();
        showError('Passwords do not match');
        confirmField.focus();
        return;
    }
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check which form is present and initialize it
    const loginForm = document.getElementById('login-form');
    const registrationForm = document.getElementById('registration-form');
    
    if (loginForm) {
        initializeLoginForm('login-form');
    }
    
    if (registrationForm) {
        initializeRegistrationForm('registration-form');
    }
});

// Export for use in other modules
export {
    initializeLoginForm,
    initializeRegistrationForm,
    initializePasswordVisibility
};
