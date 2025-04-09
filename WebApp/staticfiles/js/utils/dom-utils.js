/**
 * Task Manager - DOM Utilities
 * Common DOM manipulation and utility functions
 */

/**
 * Get an element by ID
 * @param {string} id - The element ID
 * @returns {Element|null} The element or null if not found
 */
export function getById(id) {
    return document.getElementById(id);
}

/**
 * Query selector wrapper
 * @param {string} selector - CSS selector
 * @param {Element|Document} [parent=document] - Parent element to query within
 * @returns {Element|null} The first matching element or null
 */
export function query(selector, parent = document) {
    return parent.querySelector(selector);
}

/**
 * Query selector all wrapper
 * @param {string} selector - CSS selector
 * @param {Element|Document} [parent=document] - Parent element to query within
 * @returns {NodeList} List of matching elements
 */
export function queryAll(selector, parent = document) {
    return parent.querySelectorAll(selector);
}

/**
 * Create an element with attributes and children
 * @param {string} tag - The tag name
 * @param {Object} [attrs={}] - Attributes to set on the element
 * @param {Array|Element|string} [children] - Child elements or text content
 * @returns {Element} The created element
 */
export function createElement(tag, attrs = {}, children) {
    const element = document.createElement(tag);
    
    // Set attributes
    Object.entries(attrs).forEach(([key, value]) => {
        if (key === 'className') {
            element.className = value;
        } else if (key === 'style' && typeof value === 'object') {
            Object.entries(value).forEach(([prop, val]) => {
                element.style[prop] = val;
            });
        } else if (key.startsWith('on') && typeof value === 'function') {
            const eventName = key.substring(2).toLowerCase();
            element.addEventListener(eventName, value);
        } else {
            element.setAttribute(key, value);
        }
    });
    
    // Add children
    if (children) {
        if (Array.isArray(children)) {
            children.forEach(child => {
                if (child) {
                    element.appendChild(
                        typeof child === 'string' ? document.createTextNode(child) : child
                    );
                }
            });
        } else if (typeof children === 'string') {
            element.textContent = children;
        } else {
            element.appendChild(children);
        }
    }
    
    return element;
}

/**
 * Add event listener with automatic cleanup
 * @param {Element} element - The element to attach the listener to
 * @param {string} event - The event name
 * @param {Function} callback - The event handler
 * @param {Object} [options] - Event listener options
 * @returns {Function} Function to remove the event listener
 */
export function addEvent(element, event, callback, options) {
    element.addEventListener(event, callback, options);
    return () => element.removeEventListener(event, callback, options);
}

/**
 * Add multiple event listeners with automatic cleanup
 * @param {Element} element - The element to attach listeners to
 * @param {Object} events - Object with event names as keys and callbacks as values
 * @param {Object} [options] - Event listener options
 * @returns {Function} Function to remove all event listeners
 */
export function addEvents(element, events, options) {
    const removers = Object.entries(events).map(([event, callback]) => 
        addEvent(element, event, callback, options)
    );
    
    return () => removers.forEach(remove => remove());
}

/**
 * Toggle a class on an element
 * @param {Element} element - The element
 * @param {string} className - The class to toggle
 * @param {boolean} [force] - Force add or remove
 * @returns {boolean} Whether the class is now present
 */
export function toggleClass(element, className, force) {
    return element.classList.toggle(className, force);
}

/**
 * Add classes to an element
 * @param {Element} element - The element
 * @param {...string} classNames - Classes to add
 */
export function addClass(element, ...classNames) {
    element.classList.add(...classNames);
}

/**
 * Remove classes from an element
 * @param {Element} element - The element
 * @param {...string} classNames - Classes to remove
 */
export function removeClass(element, ...classNames) {
    element.classList.remove(...classNames);
}

/**
 * Check if an element has a class
 * @param {Element} element - The element
 * @param {string} className - The class to check
 * @returns {boolean} Whether the element has the class
 */
export function hasClass(element, className) {
    return element.classList.contains(className);
}

/**
 * Set or get data attribute
 * @param {Element} element - The element
 * @param {string} key - The data attribute name (without 'data-')
 * @param {string} [value] - The value to set (omit to get)
 * @returns {string|undefined} The attribute value when getting
 */
export function data(element, key, value) {
    if (value === undefined) {
        return element.dataset[key];
    }
    element.dataset[key] = value;
}

/**
 * Debounce a function
 * @param {Function} func - The function to debounce
 * @param {number} wait - The debounce delay in milliseconds
 * @returns {Function} The debounced function
 */
export function debounce(func, wait) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

/**
 * Throttle a function
 * @param {Function} func - The function to throttle
 * @param {number} limit - The throttle limit in milliseconds
 * @returns {Function} The throttled function
 */
export function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
