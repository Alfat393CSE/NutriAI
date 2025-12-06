// History Page JavaScript

let currentFilter = 'all';
let weeklyChart = null;

document.addEventListener('DOMContentLoaded', async () => {
    await loadHistory();
    await loadHistoryStats();
    await loadWeeklyReport();
});

// Load history with optional filter
async function loadHistory() {
    try {
        const days = document.getElementById('timePeriod').value;
        const params = new URLSearchParams({ days });
        
        if (currentFilter !== 'all') {
            params.append('action_type', currentFilter);
        }
        
        const data = await window.nutriAI.apiRequest(`/api/history?${params}`);
        displayHistory(data.history);
    } catch (error) {
        document.getElementById('historyFeed').innerHTML = '<p class="text-center">Failed to load history</p>';
    }
}

// Display history entries
function displayHistory(history) {
    const feed = document.getElementById('historyFeed');
    
    if (history.length === 0) {
        feed.innerHTML = '<p class="text-center text-secondary">No activity found</p>';
        return;
    }
    
    feed.innerHTML = history.map(entry => {
        const icon = getActionIcon(entry.action_type);
        const color = getActionColor(entry.action_type);
        const timeAgo = formatTimeAgo(new Date(entry.timestamp));
        
        return `
            <div class="history-item">
                <div class="history-icon" style="background: ${color};">
                    <i class="fas fa-${icon}"></i>
                </div>
                <div class="history-content">
                    <div class="history-action">
                        <strong>${formatAction(entry.action_type)}</strong>
                        ${entry.food_name ? `<span class="food-name">${entry.food_name}</span>` : ''}
                    </div>
                    ${entry.search_query ? `<div class="history-detail">Searched: "${entry.search_query}"</div>` : ''}
                    ${entry.recommendation_reason ? `<div class="history-detail">${entry.recommendation_reason}</div>` : ''}
                    ${entry.quantity_g ? `<div class="history-detail">Quantity: ${entry.quantity_g}g</div>` : ''}
                    ${entry.calories ? `
                        <div class="history-nutrition">
                            <span><i class="fas fa-fire"></i> ${Math.round(entry.calories)}cal</span>
                            ${entry.protein_g ? `<span><i class="fas fa-dumbbell"></i> ${Math.round(entry.protein_g)}g protein</span>` : ''}
                        </div>
                    ` : ''}
                    <div class="history-time">${timeAgo}</div>
                </div>
            </div>
        `;
    }).join('');
}

// Load history statistics
async function loadHistoryStats() {
    try {
        const days = document.getElementById('timePeriod').value;
        const stats = await window.nutriAI.apiRequest(`/api/history/stats?days=${days}`);
        
        document.getElementById('totalActivities').textContent = stats.total_activities;
        document.getElementById('uniqueFoods').textContent = stats.unique_foods_explored;
        document.getElementById('totalCalories').textContent = Math.round(stats.nutritional_totals.calories);
        document.getElementById('totalProtein').textContent = Math.round(stats.nutritional_totals.protein_g) + 'g';
        
        // Display top viewed foods
        displayTopFoods(stats.top_viewed_foods);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Display top viewed foods
function displayTopFoods(topFoods) {
    const container = document.getElementById('topFoodsList');
    
    if (topFoods.length === 0) {
        container.innerHTML = '<p class="text-center text-secondary">No data yet</p>';
        return;
    }
    
    container.innerHTML = topFoods.map((item, index) => `
        <div class="top-food-item">
            <div class="rank">#${index + 1}</div>
            <div class="food-info">
                <div class="food-name">${item.name}</div>
                <div class="view-count">${item.views} views</div>
            </div>
        </div>
    `).join('');
}

// Load weekly report
async function loadWeeklyReport() {
    try {
        const report = await window.nutriAI.apiRequest('/api/history/weekly-report');
        
        const labels = report.daily_breakdown.map(d => d.day_name.substring(0, 3));
        const caloriesData = report.daily_breakdown.map(d => d.calories);
        const proteinData = report.daily_breakdown.map(d => d.protein_g);
        const activitiesData = report.daily_breakdown.map(d => d.activities);
        
        const ctx = document.getElementById('weeklyChart');
        
        if (weeklyChart) {
            weeklyChart.destroy();
        }
        
        weeklyChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Calories',
                        data: caloriesData,
                        backgroundColor: 'rgba(102, 126, 234, 0.7)',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 2,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Protein (g)',
                        data: proteinData,
                        backgroundColor: 'rgba(34, 197, 94, 0.7)',
                        borderColor: 'rgba(34, 197, 94, 1)',
                        borderWidth: 2,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Activities',
                        data: activitiesData,
                        type: 'line',
                        backgroundColor: 'rgba(249, 115, 22, 0.2)',
                        borderColor: 'rgba(249, 115, 22, 1)',
                        borderWidth: 2,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += Math.round(context.parsed.y * 100) / 100;
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Calories / Protein (g)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Activities'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Failed to load weekly report:', error);
    }
}

// Filter history by action type
function filterHistory(actionType) {
    currentFilter = actionType;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    loadHistory();
}

// Helper functions
function getActionIcon(actionType) {
    const icons = {
        'search': 'search',
        'view': 'eye',
        'log': 'check-circle',
        'recommend': 'lightbulb',
        'select': 'hand-pointer'
    };
    return icons[actionType] || 'circle';
}

function getActionColor(actionType) {
    const colors = {
        'search': 'linear-gradient(135deg, #667eea, #764ba2)',
        'view': 'linear-gradient(135deg, #4facfe, #00f2fe)',
        'log': 'linear-gradient(135deg, #43e97b, #38f9d7)',
        'recommend': 'linear-gradient(135deg, #f093fb, #f5576c)',
        'select': 'linear-gradient(135deg, #fa709a, #fee140)'
    };
    return colors[actionType] || 'linear-gradient(135deg, #9ca3af, #6b7280)';
}

function formatAction(actionType) {
    const actions = {
        'search': 'Searched',
        'view': 'Viewed',
        'log': 'Logged',
        'recommend': 'Recommended',
        'select': 'Selected'
    };
    return actions[actionType] || actionType;
}

function formatTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };
    
    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
        }
    }
    
    return 'Just now';
}
