'use strict';

// Status chart initialization
function initializeStatusChart(data) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Not Started', 'In Progress', 'Completed'],
            datasets: [{
                data: data,
                backgroundColor: [
                    '#ff6b6b',
                    '#4ecdc4',
                    '#45b7d1'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Fetch and update chart data
async function updateChartData() {
    try {
        const response = await fetch('/api/status-chart/');
        const data = await response.json();
        initializeStatusChart(data.status_counts);
    } catch (error) {
        console.error('Error fetching chart data:', error);
    }
}