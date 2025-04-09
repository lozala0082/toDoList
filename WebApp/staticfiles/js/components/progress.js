/**
 * @fileoverview Task Manager - Progress Component
 * Handles progress indicators, both circular and linear
 */

/**
 * Initialize all progress indicators
 */
function initializeProgressIndicators() {
  initializeCircularProgress();
  initializeLinearProgress();
}

/**
 * Initialize circular progress indicators
 */
function initializeCircularProgress() {
  const circularProgressElements = document.querySelectorAll('.md3-circular-progress');

  circularProgressElements.forEach(element => {
    // Clear the element first to avoid duplicates
    element.innerHTML = '';

    // Create SVG container
    const svgContainer = document.createElement('div');
    svgContainer.className = 'md3-circular-progress__svg-container';
    element.appendChild(svgContainer);

    // Create SVG element
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 100 100');
    svgContainer.appendChild(svg);

    // Create track circle
    const trackCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    trackCircle.setAttribute('cx', '50');
    trackCircle.setAttribute('cy', '50');
    trackCircle.setAttribute('r', '45');
    trackCircle.setAttribute('fill', 'none');
    trackCircle.setAttribute('stroke-width', '4');
    trackCircle.className = 'md3-circular-progress__determinate-track';
    svg.appendChild(trackCircle);

    // Create progress circle
    const progressCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    progressCircle.setAttribute('cx', '50');
    progressCircle.setAttribute('cy', '50');
    progressCircle.setAttribute('r', '45');
    progressCircle.setAttribute('fill', 'none');
    progressCircle.setAttribute('stroke-width', '4');
    progressCircle.setAttribute('stroke-linecap', 'round');
    progressCircle.className = 'md3-circular-progress__determinate-circle';
    svg.appendChild(progressCircle);

    // Get percentage from data attribute or default to 0
    const percentage = parseFloat(element.dataset.percentage || 0);

    // Calculate the stroke-dashoffset
    const circumference = 2 * Math.PI * 45;
    progressCircle.setAttribute('stroke-dasharray', circumference);
    const dashoffset = circumference - (percentage / 100 * circumference);
    progressCircle.setAttribute('stroke-dashoffset', dashoffset);

    // Create label
    const label = document.createElement('div');
    label.className = 'md3-circular-progress__label';
    label.textContent = `${Math.round(percentage)}%`;
    element.appendChild(label);
  });
}

/**
 * Initialize linear progress indicators
 */
function initializeLinearProgress() {
  const linearProgressElements = document.querySelectorAll('.md3-linear-progress');

  linearProgressElements.forEach(element => {
    const progressBar = element.querySelector('.md3-linear-progress__bar--determinate');
    if (!progressBar) return;

    // Get percentage from data attribute or default to 0
    const percentage = parseFloat(element.dataset.percentage || 0);

    // Set the transform scale
    progressBar.style.transform = `scaleX(${percentage / 100})`;
  });
}

/**
 * Update a circular progress indicator
 * @param {(string|!Element)} element The progress element or its ID
 * @param {number} percentage The percentage value (0-100)
 */
function updateCircularProgress(element, percentage) {
  // Get the element if a string ID was provided
  if (typeof element === 'string') {
    element = document.getElementById(element);
  }

  if (!element) return;

  // Update the data attribute
  element.dataset.percentage = percentage;

  // Find the progress circle
  const progressCircle = element.querySelector('.md3-circular-progress__determinate-circle');

  // If the progress circle doesn't exist, reinitialize the entire component
  if (!progressCircle) {
    initializeCircularProgress();
    return;
  }

  // Calculate the stroke-dashoffset
  const circumference = 2 * Math.PI * 45;
  const dashoffset = circumference - (percentage / 100 * circumference);

  // Set the stroke-dashoffset
  progressCircle.setAttribute('stroke-dashoffset', dashoffset);

  // Update the label text
  const label = element.querySelector('.md3-circular-progress__label');
  if (label) {
    label.textContent = `${Math.round(percentage)}%`;
  }
}

/**
 * Update a linear progress indicator
 * @param {(string|!Element)} element The progress element or its ID
 * @param {number} percentage The percentage value (0-100)
 */
function updateLinearProgress(element, percentage) {
  // Get the element if a string ID was provided
  if (typeof element === 'string') {
    element = document.getElementById(element);
  }

  if (!element) return;

  // Find the progress bar
  const progressBar = element.querySelector('.md3-linear-progress__bar--determinate');
  if (!progressBar) return;

  // Set the transform scale
  progressBar.style.transform = `scaleX(${percentage / 100})`;

  // Update the data attribute
  element.dataset.percentage = percentage;
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', initializeProgressIndicators);

// Export for use in other modules
export {
  initializeProgressIndicators,
  updateCircularProgress,
  updateLinearProgress
};
