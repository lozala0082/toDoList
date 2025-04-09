/**
 * @fileoverview Task Manager - Forms Component
 * Handles form interactions, validation, and dynamic form elements
 */

import {showError} from './snackbar.js';

/**
 * Initialize all form components
 */
function initializeForms() {
  initializeTextFields();
  initializeCheckboxes();
  initializeSelects();
  initializeAdvancedMode();
  initializeSubtaskForms();
  initializeFormValidation();
  initializeFormStorage();
}

/**
 * Initialize Material Design text fields
 */
function initializeTextFields() {
  document.querySelectorAll('.mdc-text-field').forEach(textField => {
    if (textField) window.mdc.textField.MDCTextField.attachTo(textField);
  });
}

/**
 * Initialize Material Design checkboxes
 */
function initializeCheckboxes() {
  document.querySelectorAll('.mdc-checkbox').forEach(checkbox => {
    if (checkbox) window.mdc.checkbox.MDCCheckbox.attachTo(checkbox);
  });
}

/**
 * Initialize Material Design select menus
 */
function initializeSelects() {
  document.querySelectorAll('.mdc-select').forEach(select => {
    if (select) window.mdc.select.MDCSelect.attachTo(select);
  });
}

/**
 * Initialize advanced mode toggle for assignment forms
 */
function initializeAdvancedMode() {
    const advancedModeSwitch = document.getElementById('advanced-mode-switch');
    if (!advancedModeSwitch) return;

    const subtasksSection = document.getElementById('subtasks-section');
    const statusField = document.getElementById('id_status');
    const statusFieldContainer = statusField ? statusField.closest('.form-field-container') : null;

    // Set initial state
    if (subtasksSection) {
        subtasksSection.style.display = advancedModeSwitch.checked ? 'block' : 'none';
    }

    // Add change event listener
    advancedModeSwitch.addEventListener('change', function() {
        if (subtasksSection) {
            subtasksSection.style.display = this.checked ? 'block' : 'none';
        }

        // Update status field
        if (statusFieldContainer && statusField) {
            if (this.checked) {
                statusField.disabled = true;
                if (!statusFieldContainer.querySelector('.status-help-text')) {
                    const helpText = document.createElement('div');
                    helpText.className = 'mdc-text-field-helper-text status-help-text';
                    helpText.textContent = 'Status is automatically determined by subtask completion';
                    statusFieldContainer.appendChild(helpText);
                }
            } else {
                statusField.disabled = false;
                const helpText = statusFieldContainer.querySelector('.status-help-text');
                if (helpText) helpText.remove();
            }
        }
    });
}

/**
 * Initialize subtask form functionality
 */
function initializeSubtaskForms() {
    const subtaskContainer = document.getElementById('subtask-container');
    if (!subtaskContainer) return;

    const addSubtaskButton = document.getElementById('add-subtask-button');
    if (!addSubtaskButton) return;

    // Add click event listener to add new subtask
    addSubtaskButton.addEventListener('click', function(e) {
        e.preventDefault();

        // Get the current number of subtasks
        const subtaskItems = subtaskContainer.querySelectorAll('.subtask-item');
        const newIndex = subtaskItems.length;

        // Create new subtask item
        const subtaskItem = document.createElement('div');
        subtaskItem.className = 'subtask-item';
        subtaskItem.innerHTML = `
            <div class="subtask-item__input">
                <div class="mdc-text-field mdc-text-field--outlined">
                    <input type="text" id="id_subtasks-${newIndex}-name" name="subtasks-${newIndex}-name" class="mdc-text-field__input" required>
                    <div class="mdc-notched-outline">
                        <div class="mdc-notched-outline__leading"></div>
                        <div class="mdc-notched-outline__notch">
                            <label for="id_subtasks-${newIndex}-name" class="mdc-floating-label">Subtask name</label>
                        </div>
                        <div class="mdc-notched-outline__trailing"></div>
                    </div>
                </div>
            </div>
            <div class="subtask-item__checkbox">
                <div class="mdc-checkbox">
                    <input type="checkbox" id="id_subtasks-${newIndex}-is_completed" name="subtasks-${newIndex}-is_completed" class="mdc-checkbox__native-control">
                    <div class="mdc-checkbox__background">
                        <svg class="mdc-checkbox__checkmark" viewBox="0 0 24 24">
                            <path class="mdc-checkbox__checkmark-path" fill="none" d="M1.73,12.91 8.1,19.28 22.79,4.59"></path>
                        </svg>
                        <div class="mdc-checkbox__mixedmark"></div>
                    </div>
                    <div class="mdc-checkbox__ripple"></div>
                </div>
            </div>
            <button type="button" class="subtask-item__remove material-symbols-outlined" aria-label="Remove subtask">close</button>
        `;

        // Add to container
        subtaskContainer.appendChild(subtaskItem);

        // Initialize Material Design components
        const textField = subtaskItem.querySelector('.mdc-text-field');
        if (textField) window.mdc.textField.MDCTextField.attachTo(textField);

        const checkbox = subtaskItem.querySelector('.mdc-checkbox');
        if (checkbox) window.mdc.checkbox.MDCCheckbox.attachTo(checkbox);

        // Add remove button event listener
        const removeButton = subtaskItem.querySelector('.subtask-item__remove');
        if (removeButton) {
            removeButton.addEventListener('click', function() {
                subtaskItem.remove();
                updateSubtaskIndices();
            });
        }

        // Update the form management field
        updateSubtaskFormManagement();
    });

    // Add event listeners to existing remove buttons
    document.querySelectorAll('.subtask-item__remove').forEach(button => {
        button.addEventListener('click', function() {
            const subtaskItem = this.closest('.subtask-item');
            if (subtaskItem) {
                subtaskItem.remove();
                updateSubtaskIndices();
            }
        });
    });
}

/**
 * Update subtask indices after removal
 */
function updateSubtaskIndices() {
    const subtaskContainer = document.getElementById('subtask-container');
    if (!subtaskContainer) return;

    const subtaskItems = subtaskContainer.querySelectorAll('.subtask-item');

    subtaskItems.forEach((item, index) => {
        // Update input name and id
        const nameInput = item.querySelector('input[name^="subtasks-"][name$="-name"]');
        if (nameInput) {
            nameInput.name = `subtasks-${index}-name`;
            nameInput.id = `id_subtasks-${index}-name`;
        }

        // Update checkbox name and id
        const checkbox = item.querySelector('input[name^="subtasks-"][name$="-is_completed"]');
        if (checkbox) {
            checkbox.name = `subtasks-${index}-is_completed`;
            checkbox.id = `id_subtasks-${index}-is_completed`;
        }

        // Update label for attribute
        const label = item.querySelector('label[for^="id_subtasks-"]');
        if (label && nameInput) {
            label.setAttribute('for', nameInput.id);
        }
    });

    // Update the form management field
    updateSubtaskFormManagement();
}

/**
 * Update the subtask formset management form
 */
function updateSubtaskFormManagement() {
    const subtaskContainer = document.getElementById('subtask-container');
    if (!subtaskContainer) return;

    const subtaskItems = subtaskContainer.querySelectorAll('.subtask-item');
    const totalFormsInput = document.getElementById('id_subtasks-TOTAL_FORMS');

    if (totalFormsInput) {
        totalFormsInput.value = subtaskItems.length;
    }
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Check for required fields
            const requiredFields = form.querySelectorAll('[required]');
            let hasError = false;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    hasError = true;

                    // Find the field container
                    const fieldContainer = field.closest('.form-field-container');
                    if (fieldContainer) {
                        // Check if error message already exists
                        if (!fieldContainer.querySelector('.errorlist')) {
                            const errorList = document.createElement('div');
                            errorList.className = 'errorlist';
                            errorList.innerHTML = '<span>This field is required.</span>';
                            fieldContainer.appendChild(errorList);
                        }
                    }

                    // Add error class to text field
                    const textField = field.closest('.mdc-text-field');
                    if (textField) {
                        textField.classList.add('mdc-text-field--invalid');
                    }
                }
            });

            if (hasError) {
                e.preventDefault();
                showError('Please fill in all required fields.');

                // Scroll to first error
                const firstError = form.querySelector('.errorlist');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
}

/**
 * Initialize form storage for saving form data in localStorage
 * @param {string=} formId The ID of the form element
 * @param {!Object=} fieldConfig Configuration for fields to store
 */
function initializeFormStorage(formId = 'assignment-form', fieldConfig = {
  'id_due_date': 'assignment_due_date',
  'id_name': 'assignment_name',
  'id_description': 'assignment_description'
}) {
  const form = document.getElementById(formId);
  if (!form) return;

  // Track which fields have been stored
  const storedFields = [];

  // Check if there are validation errors on the form
  const hasErrors = form.querySelector('.error-message') !== null;
  console.log('Form has validation errors:', hasErrors);

  // Process each field in the configuration
  Object.entries(fieldConfig).forEach(([fieldId, storageKey]) => {
    const field = document.getElementById(fieldId);
    if (!field) return;

    // Store field data in localStorage when it changes
    field.addEventListener('change', function() {
      localStorage.setItem(storageKey, this.value);
    });

    // Only restore from localStorage if there are validation errors
    // or if the field is empty and we have a saved value
    if (hasErrors && localStorage.getItem(storageKey)) {
      field.value = localStorage.getItem(storageKey);
    }

    // Add to stored fields list
    storedFields.push(storageKey);
  });

  // Clear localStorage on successful form submission
  if (storedFields.length > 0) {
    form.addEventListener('submit', function() {
      // We'll clear storage immediately to prevent it from being used on the next form
      storedFields.forEach(key => localStorage.removeItem(key));
    });

    // Also clear storage when the form is loaded if there are no validation errors
    if (!hasErrors) {
      storedFields.forEach(key => localStorage.removeItem(key));
    }
  }
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', initializeForms);

// Export for use in other modules
export {
  initializeForms,
  initializeTextFields,
  initializeCheckboxes,
  initializeSelects,
  initializeAdvancedMode,
  initializeSubtaskForms,
  initializeFormStorage,
  initializeFormValidation
};
