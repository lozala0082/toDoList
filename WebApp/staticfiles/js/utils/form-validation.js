/**
 * Task Manager - Form Validation Utilities
 * Functions for validating form inputs
 */

import { showError } from '../components/snackbar.js';

/**
 * Validate a required field
 * @param {HTMLInputElement|HTMLSelectElement|HTMLTextAreaElement} field - The field to validate
 * @returns {boolean} Whether the field is valid
 */
export function validateRequired(field) {
    const value = field.value.trim();
    const isValid = value !== '';
    
    if (!isValid) {
        markFieldInvalid(field, 'This field is required');
    } else {
        markFieldValid(field);
    }
    
    return isValid;
}

/**
 * Validate an email field
 * @param {HTMLInputElement} field - The email field to validate
 * @returns {boolean} Whether the field is valid
 */
export function validateEmail(field) {
    const value = field.value.trim();
    
    // Skip validation if empty (use validateRequired for required fields)
    if (value === '') {
        markFieldValid(field);
        return true;
    }
    
    // Simple email regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(value);
    
    if (!isValid) {
        markFieldInvalid(field, 'Please enter a valid email address');
    } else {
        markFieldValid(field);
    }
    
    return isValid;
}

/**
 * Validate a date field
 * @param {HTMLInputElement} field - The date field to validate
 * @returns {boolean} Whether the field is valid
 */
export function validateDate(field) {
    const value = field.value.trim();
    
    // Skip validation if empty (use validateRequired for required fields)
    if (value === '') {
        markFieldValid(field);
        return true;
    }
    
    const date = new Date(value);
    const isValid = !isNaN(date.getTime());
    
    if (!isValid) {
        markFieldInvalid(field, 'Please enter a valid date');
    } else {
        markFieldValid(field);
    }
    
    return isValid;
}

/**
 * Validate a password field
 * @param {HTMLInputElement} field - The password field to validate
 * @param {Object} [options] - Validation options
 * @param {number} [options.minLength=8] - Minimum password length
 * @param {boolean} [options.requireSpecialChar=false] - Whether to require a special character
 * @param {boolean} [options.requireNumber=false] - Whether to require a number
 * @param {boolean} [options.requireUppercase=false] - Whether to require an uppercase letter
 * @returns {boolean} Whether the field is valid
 */
export function validatePassword(field, options = {}) {
    const {
        minLength = 8,
        requireSpecialChar = false,
        requireNumber = false,
        requireUppercase = false
    } = options;
    
    const value = field.value;
    
    // Skip validation if empty (use validateRequired for required fields)
    if (value === '') {
        markFieldValid(field);
        return true;
    }
    
    let isValid = true;
    let errorMessage = '';
    
    // Check minimum length
    if (value.length < minLength) {
        isValid = false;
        errorMessage = `Password must be at least ${minLength} characters`;
    }
    
    // Check for special character
    if (isValid && requireSpecialChar && !/[!@#$%^&*(),.?":{}|<>]/.test(value)) {
        isValid = false;
        errorMessage = 'Password must include at least one special character';
    }
    
    // Check for number
    if (isValid && requireNumber && !/\d/.test(value)) {
        isValid = false;
        errorMessage = 'Password must include at least one number';
    }
    
    // Check for uppercase letter
    if (isValid && requireUppercase && !/[A-Z]/.test(value)) {
        isValid = false;
        errorMessage = 'Password must include at least one uppercase letter';
    }
    
    if (!isValid) {
        markFieldInvalid(field, errorMessage);
    } else {
        markFieldValid(field);
    }
    
    return isValid;
}

/**
 * Validate password confirmation
 * @param {HTMLInputElement} confirmField - The confirmation field
 * @param {HTMLInputElement} passwordField - The password field
 * @returns {boolean} Whether the fields match
 */
export function validatePasswordConfirmation(confirmField, passwordField) {
    const confirmValue = confirmField.value;
    const passwordValue = passwordField.value;
    
    // Skip validation if empty (use validateRequired for required fields)
    if (confirmValue === '') {
        markFieldValid(confirmField);
        return true;
    }
    
    const isValid = confirmValue === passwordValue;
    
    if (!isValid) {
        markFieldInvalid(confirmField, 'Passwords do not match');
    } else {
        markFieldValid(confirmField);
    }
    
    return isValid;
}

/**
 * Mark a field as invalid
 * @param {HTMLElement} field - The field to mark
 * @param {string} message - The error message
 */
export function markFieldInvalid(field, message) {
    // Find the field container
    const fieldContainer = field.closest('.form-field-container');
    if (!fieldContainer) return;
    
    // Check if error message already exists
    let errorList = fieldContainer.querySelector('.errorlist');
    
    if (!errorList) {
        // Create error list
        errorList = document.createElement('div');
        errorList.className = 'errorlist';
        fieldContainer.appendChild(errorList);
    }
    
    // Set error message
    errorList.innerHTML = `<span>${message}</span>`;
    
    // Add error class to text field
    const textField = field.closest('.mdc-text-field');
    if (textField) {
        textField.classList.add('mdc-text-field--invalid');
    }
}

/**
 * Mark a field as valid
 * @param {HTMLElement} field - The field to mark
 */
export function markFieldValid(field) {
    // Find the field container
    const fieldContainer = field.closest('.form-field-container');
    if (!fieldContainer) return;
    
    // Remove error list
    const errorList = fieldContainer.querySelector('.errorlist');
    if (errorList) {
        errorList.remove();
    }
    
    // Remove error class from text field
    const textField = field.closest('.mdc-text-field');
    if (textField) {
        textField.classList.remove('mdc-text-field--invalid');
    }
}

/**
 * Validate a form
 * @param {HTMLFormElement} form - The form to validate
 * @returns {boolean} Whether the form is valid
 */
export function validateForm(form) {
    // Get all required fields
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    // Validate each required field
    requiredFields.forEach(field => {
        if (!validateRequired(field)) {
            isValid = false;
        }
    });
    
    // Get all email fields
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (!validateEmail(field)) {
            isValid = false;
        }
    });
    
    // Get all date fields
    const dateFields = form.querySelectorAll('input[type="date"]');
    dateFields.forEach(field => {
        if (!validateDate(field)) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        showError('Please correct the errors in the form');
        
        // Scroll to first error
        const firstError = form.querySelector('.errorlist');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
    
    return isValid;
}

/**
 * Initialize form validation
 * @param {HTMLFormElement} form - The form to initialize
 * @param {Object} [options] - Validation options
 */
export function initializeFormValidation(form, options = {}) {
    // Add submit event listener
    form.addEventListener('submit', function(e) {
        if (!validateForm(form)) {
            e.preventDefault();
        }
    });
    
    // Add input event listeners for real-time validation
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', () => {
            validateRequired(field);
        });
    });
    
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        field.addEventListener('blur', () => {
            validateEmail(field);
        });
    });
    
    const dateFields = form.querySelectorAll('input[type="date"]');
    dateFields.forEach(field => {
        field.addEventListener('blur', () => {
            validateDate(field);
        });
    });
}
