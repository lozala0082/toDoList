/**
 * Task Manager - Main JavaScript
 * Entry point for all JavaScript functionality
 */

// Import component scripts
import { initializeSnackbar } from './components/snackbar.js';
import './components/forms.js';
import './components/progress.js';

// Import form handlers
import './forms/assignment-form.js';
import './forms/auth-forms.js';

// Initialize Material Design components
document.addEventListener('DOMContentLoaded', function() {
    // Auto-initialize all MDC components
    window.mdc.autoInit();

    // Initialize any custom components
    initializeCustomComponents();
});

/**
 * Initialize any custom components not handled by MDC auto-init
 */
function initializeCustomComponents() {
    // Initialize ripples on list items
    document.querySelectorAll('.mdc-list-item').forEach(listItem => {
        if (listItem) window.mdc.ripple.MDCRipple.attachTo(listItem);
    });

    // Initialize text fields
    document.querySelectorAll('.mdc-text-field').forEach(textField => {
        if (textField) window.mdc.textField.MDCTextField.attachTo(textField);
    });

    // Initialize checkboxes
    document.querySelectorAll('.mdc-checkbox').forEach(checkbox => {
        if (checkbox) window.mdc.checkbox.MDCCheckbox.attachTo(checkbox);
    });

    // Initialize select menus
    document.querySelectorAll('.mdc-select').forEach(select => {
        if (select) window.mdc.select.MDCSelect.attachTo(select);
    });
}
