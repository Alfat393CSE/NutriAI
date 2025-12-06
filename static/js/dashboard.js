// Dashboard JavaScript

let dashboardData = null;
let macrosChart = null;
let weeklyChart = null;

// Load dashboard data on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadDashboardStats();
    await loadTodayMeals();
    initializeCharts();
});

// Load dashboard statistics
async function loadDashboardStats() {
    try {
        const data = await window.nutriAI.apiRequest('/api/dashboard/stats');
        dashboardData = data;
        
        // Update stats
        document.getElementById('todayCalories').textContent = data.today.calories;
        document.getElementById('targetCalories').textContent = data.today.target_calories;
        document.getElementById('todayProtein').textContent = data.today.protein + 'g';
        document.getElementById('todayCarbs').textContent = data.today.carbs + 'g';
        document.getElementById('todayFat').textContent = data.today.fat + 'g';
        
        // Update progress bar
        const progress = (data.today.calories / data.today.target_calories) * 100;
        document.getElementById('caloriesProgress').style.width = Math.min(progress, 100) + '%';
        
        // Update active meal plan
        if (data.active_meal_plan) {
            displayActiveMealPlan(data.active_meal_plan);
        }
        
    } catch (error) {
        console.error('Failed to load dashboard stats:', error);
    }
}

// Load today's meals
async function loadTodayMeals() {
    try {
        const today = new Date().toISOString().split('T')[0];
        const meals = await window.nutriAI.apiRequest(`/api/food-logs?date=${today}`);
        
        const mealsContainer = document.getElementById('todayMeals');
        
        if (meals.length === 0) {
            mealsContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-utensils"></i>
                    <p>No meals logged yet</p>
                    <button class="btn-primary" onclick="logFood()">Log Your First Meal</button>
                </div>
            `;
            return;
        }
        
        mealsContainer.innerHTML = meals.map(meal => `
            <div class="meal-item">
                <div class="meal-icon">
                    <i class="fas fa-${getMealIcon(meal.meal_type)}"></i>
                </div>
                <div class="meal-info">
                    <div class="meal-name">${meal.food.name}</div>
                    <div class="meal-details">${meal.quantity_g}g • ${meal.calories_consumed} cal</div>
                </div>
                <div class="meal-time">${meal.meal_type}</div>
                <button class="btn-icon-sm" onclick="deleteMeal(${meal.id})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Failed to load meals:', error);
    }
}

function getMealIcon(mealType) {
    const icons = {
        'Breakfast': 'coffee',
        'Lunch': 'hamburger',
        'Dinner': 'pizza-slice',
        'Snack': 'cookie'
    };
    return icons[mealType] || 'utensils';
}

// Display active meal plan
function displayActiveMealPlan(plan) {
    const container = document.getElementById('activeMealPlan');
    container.innerHTML = `
        <div class="meal-plan-card">
            <h4>${plan.name || 'Current Meal Plan'}</h4>
            <div class="meal-plan-stats">
                <div class="plan-stat">
                    <span class="stat-label">Weekly Calories</span>
                    <span class="stat-value">${plan.total_calories}</span>
                </div>
                <div class="plan-stat">
                    <span class="stat-label">Protein</span>
                    <span class="stat-value">${plan.total_protein}g</span>
                </div>
            </div>
            <a href="/meal-planner" class="btn-primary btn-block mt-2">View Full Plan</a>
        </div>
    `;
}

// Initialize charts
function initializeCharts() {
    // Macros Chart
    const macrosCtx = document.getElementById('macrosChart');
    if (macrosCtx && dashboardData) {
        macrosChart = new Chart(macrosCtx, {
            type: 'doughnut',
            data: {
                labels: ['Protein', 'Carbs', 'Fat'],
                datasets: [{
                    data: [
                        dashboardData.today.protein,
                        dashboardData.today.carbs,
                        dashboardData.today.fat
                    ],
                    backgroundColor: [
                        '#22c55e',
                        '#f97316',
                        '#3b82f6'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Weekly Progress Chart
    const weeklyCtx = document.getElementById('weeklyChart');
    if (weeklyCtx) {
        weeklyChart = new Chart(weeklyCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Calories',
                    data: [1800, 2100, 1950, 2200, 1900, 2000, 1850],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Log food modal
function logFood() {
    const modal = document.getElementById('logFoodModal');
    modal.classList.add('active');
    
    // Setup food search
    const searchInput = document.getElementById('foodSearch');
    const resultsContainer = document.getElementById('foodSearchResults');
    
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value;
        
        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            return;
        }
        
        searchTimeout = setTimeout(async () => {
            try {
                const data = await window.nutriAI.apiRequest(`/api/foods?search=${query}`);
                const foods = data.foods || data || [];
                displayFoodResults(foods, resultsContainer);
            } catch (error) {
                console.error('Search failed:', error);
            }
        }, 300);
    });
}

function displayFoodResults(foods, container) {
    if (foods.length === 0) {
        container.innerHTML = '<p class="text-center text-secondary">No foods found</p>';
        return;
    }
    
    container.innerHTML = foods.map(food => `
        <div class="search-result-item" onclick="selectFood(${food.id}, '${food.name}')">
            <span>${food.name}</span>
            <span class="text-secondary">${food.calories} cal</span>
        </div>
    `).join('');
}

let selectedFoodId = null;
function selectFood(id, name) {
    selectedFoodId = id;
    document.getElementById('foodSearch').value = name;
    document.getElementById('foodSearchResults').innerHTML = '';
}

// Submit food log
document.getElementById('logFoodForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!selectedFoodId) {
        window.nutriAI.showToast('Please select a food', 'error');
        return;
    }
    
    const quantity = document.getElementById('foodQuantity').value;
    const mealType = document.getElementById('mealType').value;
    const today = new Date().toISOString().split('T')[0];
    
    try {
        await window.nutriAI.apiRequest('/api/food-logs', 'POST', {
            food_id: selectedFoodId,
            quantity_g: parseFloat(quantity),
            meal_type: mealType,
            date: today
        });
        
        window.nutriAI.showToast('Food logged successfully!', 'success');
        closeModal('logFoodModal');
        await loadDashboardStats();
        await loadTodayMeals();
        
        // Reset form
        selectedFoodId = null;
        document.getElementById('logFoodForm').reset();
        
    } catch (error) {
        // Error handled by apiRequest
    }
});

// Delete meal
async function deleteMeal(id) {
    if (!confirm('Delete this meal log?')) return;
    
    try {
        await window.nutriAI.apiRequest(`/api/food-logs/${id}`, 'DELETE');
        window.nutriAI.showToast('Meal deleted', 'success');
        await loadDashboardStats();
        await loadTodayMeals();
    } catch (error) {
        // Error handled
    }
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Quick actions
async function generateMealPlan() {
    window.location.href = '/meal-planner';
}

async function weeklyReport() {
    try {
        const report = await window.nutriAI.apiRequest('/api/features/weekly-report');
        
        // Show report in modal or new page
        alert(`Weekly Report\n\nGrade: ${report.grade}\nTotal Calories: ${report.totals.calories}\nAverage Daily: ${report.averages.daily_calories}\n\n${report.insights.join('\n')}`);
    } catch (error) {
        // Error handled
    }
}

async function moodFood() {
    const mood = prompt('How are you feeling? (stressed, tired, happy, sad)');
    if (!mood) return;
    
    try {
        const result = await window.nutriAI.apiRequest('/api/features/mood-food', 'POST', { mood });
        window.nutriAI.showToast(`Try: ${result.recommendations.map(f => f.name).join(', ')}`, 'success');
    } catch (error) {
        // Error handled
    }
}

async function futurePrediction() {
    try {
        const prediction = await window.nutriAI.apiRequest('/api/features/future-prediction');
        
        // Display prediction
        console.log('Future Prediction:', prediction);
        alert(`Weight Prediction:\n\nCurrent: ${prediction.current_weight}kg\nIn 4 weeks: ${prediction.predictions[3].predicted_weight}kg\nIn 8 weeks: ${prediction.predictions[7].predicted_weight}kg`);
    } catch (error) {
        // Error handled
    }
}

function showNotifications() {
    window.nutriAI.showToast('No new notifications', 'info');
}

function showSettings() {
    window.nutriAI.showToast('Settings coming soon!', 'info');
}

function showProfile() {
    window.location.href = '/profile';
}

// Add CSS for meal items
const dashboardStyles = document.createElement('style');
dashboardStyles.textContent = `
    .meal-item {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px;
        background: var(--bg-secondary);
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .meal-icon {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--primary);
        color: white;
        border-radius: 50%;
        font-size: 1.25rem;
    }
    .meal-info {
        flex: 1;
    }
    .meal-name {
        font-weight: 600;
        color: var(--text-primary);
    }
    .meal-details {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    .meal-time {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    .search-result-item {
        display: flex;
        justify-content: space-between;
        padding: 12px;
        cursor: pointer;
        border-radius: 8px;
        transition: background 0.2s;
    }
    .search-result-item:hover {
        background: var(--bg-secondary);
    }
    .search-results {
        max-height: 300px;
        overflow-y: auto;
        margin-top: 8px;
    }
    .meal-plan-card {
        padding: 24px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--purple) 100%);
        color: white;
        border-radius: 12px;
    }
    .meal-plan-card h4 {
        color: white;
        margin-bottom: 16px;
    }
    .meal-plan-stats {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 16px;
    }
    .plan-stat {
        display: flex;
        flex-direction: column;
    }
    .plan-stat .stat-label {
        font-size: 0.875rem;
        opacity: 0.9;
    }
    .plan-stat .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
`;
document.head.appendChild(dashboardStyles);
