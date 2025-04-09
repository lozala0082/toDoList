/**
 * Task Manager - Assignment Form Handler
 * Handles the assignment creation and editing forms
 */

import { initializeFormValidation } from '../utils/form-validation.js';
import { showSuccess, showError } from '../components/snackbar.js';

/**
 * Initialize the assignment form
 * @param {string} formId - The ID of the form element
 */
export function initializeAssignmentForm(formId = 'assignment-form') {
    const form = document.getElementById(formId);
    if (!form) return;

    // Initialize form validation
    initializeFormValidation(form);

    // Initialize advanced mode toggle
    initializeAdvancedMode();

    // Initialize subtask management
    initializeSubtaskManagement();

    // Initialize form storage
    initializeFormStorage();

    // Initialize assignee selection
    initializeAssigneeSelection();

    // Add form submission handler
    form.addEventListener('submit', handleFormSubmit);
}

/**
 * Initialize advanced mode toggle
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
 * Initialize subtask management
 */
function initializeSubtaskManagement() {
    const subtaskContainer = document.getElementById('subtask-container');
    if (!subtaskContainer) return;

    const addSubtaskButton = document.getElementById('add-subtask-button');
    if (!addSubtaskButton) return;

    // Add click event listener to add new subtask
    addSubtaskButton.addEventListener('click', function(e) {
        e.preventDefault();
        addNewSubtask(subtaskContainer);
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
 * Add a new subtask to the container
 * @param {HTMLElement} container - The subtask container
 */
function addNewSubtask(container) {
    // Get the current number of subtasks
    const subtaskItems = container.querySelectorAll('.subtask-item');
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
    container.appendChild(subtaskItem);

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
 * Initialize form storage for saving form data in localStorage
 */
function initializeFormStorage() {
    // Import the shared form storage function
    import('../components/forms.js').then(module => {
        // Use the shared implementation with our specific configuration
        const fieldConfig = {
            'id_due_date': 'assignment_due_date',
            'id_name': 'assignment_name',
            'id_description': 'assignment_description',
            'id_status': 'assignment_status'
        };

        // Call the shared implementation
        if (module.initializeFormStorage) {
            module.initializeFormStorage('assignment-form', fieldConfig);
        }
    }).catch(error => {
        console.error('Error importing forms module:', error);
    });
}

/**
 * Initialize assignee selection
 */
function initializeAssigneeSelection() {
    const assigneeCheckboxes = document.querySelectorAll('input[name="assignees"]');
    if (!assigneeCheckboxes.length) return;

    // Add custom styling to checkboxes
    assigneeCheckboxes.forEach(checkbox => {
        const label = document.querySelector(`label[for="${checkbox.id}"]`);
        if (!label) return;

        // Create custom checkbox container
        const container = document.createElement('div');
        container.className = 'custom-checkbox-container';

        // Create custom checkbox
        const customCheckbox = document.createElement('span');
        customCheckbox.className = 'custom-checkbox';

        // Create checkmark
        const checkmark = document.createElement('span');
        checkmark.className = 'custom-checkbox-checkmark material-symbols-outlined';
        checkmark.textContent = 'check';
        customCheckbox.appendChild(checkmark);

        // Create label
        const customLabel = document.createElement('span');
        customLabel.className = 'custom-checkbox-label';
        customLabel.textContent = label.textContent;

        // Replace original checkbox and label
        checkbox.parentNode.insertBefore(container, checkbox);
        container.appendChild(checkbox);
        container.appendChild(customCheckbox);
        container.appendChild(customLabel);

        // Remove original label
        label.remove();
    });
}

/**
 * Handle form submission
 * @param {Event} e - The submit event
 */
function handleFormSubmit(e) {
    const form = e.target;

    // Check if advanced mode is enabled
    const advancedModeSwitch = document.getElementById('advanced-mode-switch');
    if (advancedModeSwitch && advancedModeSwitch.checked) {
        // Check if there are any subtasks
        const subtaskContainer = document.getElementById('subtask-container');
        if (subtaskContainer) {
            const subtaskItems = subtaskContainer.querySelectorAll('.subtask-item');
            if (subtaskItems.length === 0) {
                // Show warning but don't prevent submission
                showWarning('No subtasks added. Status will be set manually.');
            }
        }
    }
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeAssignmentForm();
});

// Export for use in other modules
export {
    initializeAssignmentForm,
    initializeAdvancedMode,
    initializeSubtaskManagement,
    initializeFormStorage,
    initializeAssigneeSelection
};
