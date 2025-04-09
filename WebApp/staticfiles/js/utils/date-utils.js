/**
 * Task Manager - Date Utilities
 * Functions for working with dates
 */

/**
 * Format a date as YYYY-MM-DD (for input[type="date"])
 * @param {Date} date - The date to format
 * @returns {string} The formatted date
 */
export function formatDateForInput(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/**
 * Format a date as a human-readable string
 * @param {Date|string} date - The date to format
 * @param {Object} [options] - Formatting options
 * @param {boolean} [options.includeTime=false] - Whether to include the time
 * @param {boolean} [options.includeDay=true] - Whether to include the day of week
 * @returns {string} The formatted date
 */
export function formatDate(date, options = {}) {
    const { includeTime = false, includeDay = true } = options;
    
    // Convert string to Date if needed
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return 'Invalid date';
    }
    
    const formatter = new Intl.DateTimeFormat('en-US', {
        weekday: includeDay ? 'long' : undefined,
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: includeTime ? 'numeric' : undefined,
        minute: includeTime ? '2-digit' : undefined,
        hour12: true
    });
    
    return formatter.format(date);
}

/**
 * Get the relative time string (e.g., "2 days ago", "in 3 hours")
 * @param {Date|string} date - The date to format
 * @returns {string} The relative time string
 */
export function getRelativeTimeString(date) {
    // Convert string to Date if needed
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return 'Invalid date';
    }
    
    const now = new Date();
    const diffInMs = date.getTime() - now.getTime();
    const diffInSecs = Math.round(diffInMs / 1000);
    const diffInMins = Math.round(diffInSecs / 60);
    const diffInHours = Math.round(diffInMins / 60);
    const diffInDays = Math.round(diffInHours / 24);
    
    const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
    
    if (Math.abs(diffInDays) >= 30) {
        return formatDate(date);
    } else if (Math.abs(diffInDays) >= 1) {
        return rtf.format(diffInDays, 'day');
    } else if (Math.abs(diffInHours) >= 1) {
        return rtf.format(diffInHours, 'hour');
    } else if (Math.abs(diffInMins) >= 1) {
        return rtf.format(diffInMins, 'minute');
    } else {
        return rtf.format(diffInSecs, 'second');
    }
}

/**
 * Check if a date is today
 * @param {Date|string} date - The date to check
 * @returns {boolean} Whether the date is today
 */
export function isToday(date) {
    // Convert string to Date if needed
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return false;
    }
    
    const today = new Date();
    return (
        date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear()
    );
}

/**
 * Check if a date is in the past
 * @param {Date|string} date - The date to check
 * @returns {boolean} Whether the date is in the past
 */
export function isPast(date) {
    // Convert string to Date if needed
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return false;
    }
    
    const now = new Date();
    return date < now;
}

/**
 * Check if a date is in the future
 * @param {Date|string} date - The date to check
 * @returns {boolean} Whether the date is in the future
 */
export function isFuture(date) {
    // Convert string to Date if needed
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return false;
    }
    
    const now = new Date();
    return date > now;
}

/**
 * Get the start of a day
 * @param {Date|string} date - The date
 * @returns {Date} The start of the day
 */
export function startOfDay(date) {
    // Convert string to Date if needed
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return new Date();
    }
    
    const result = new Date(date);
    result.setHours(0, 0, 0, 0);
    return result;
}

/**
 * Get the end of a day
 * @param {Date|string} date - The date
 * @returns {Date} The end of the day
 */
export function endOfDay(date) {
    // Convert string to Date if needed
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return new Date();
    }
    
    const result = new Date(date);
    result.setHours(23, 59, 59, 999);
    return result;
}

/**
 * Add days to a date
 * @param {Date|string} date - The date
 * @param {number} days - The number of days to add
 * @returns {Date} The new date
 */
export function addDays(date, days) {
    // Convert string to Date if needed
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return new Date();
    }
    
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

/**
 * Get the difference in days between two dates
 * @param {Date|string} date1 - The first date
 * @param {Date|string} date2 - The second date
 * @returns {number} The difference in days
 */
export function diffInDays(date1, date2) {
    // Convert string to Date if needed
    if (typeof date1 === 'string') {
        date1 = new Date(date1);
    }
    if (typeof date2 === 'string') {
        date2 = new Date(date2);
    }
    
    // Check if dates are valid
    if (isNaN(date1.getTime()) || isNaN(date2.getTime())) {
        return 0;
    }
    
    // Convert to UTC to avoid DST issues
    const utc1 = Date.UTC(date1.getFullYear(), date1.getMonth(), date1.getDate());
    const utc2 = Date.UTC(date2.getFullYear(), date2.getMonth(), date2.getDate());
    
    // Calculate difference in days
    return Math.floor((utc2 - utc1) / (1000 * 60 * 60 * 24));
}
