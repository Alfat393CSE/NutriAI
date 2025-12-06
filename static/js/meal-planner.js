// Enhanced Meal Planner JavaScript

let currentMealType = '';
let allFoods = [];
let currentFilter = 'all';
let todaysMeals = {
    Breakfast: [],
    Lunch: [],
    Dinner: [],
    Snack: []
};

document.addEventListener('DOMContentLoaded', async () => {
    await loadAllFoods();
    loadTodaysMeals();
    setupGeneratePlanForm();
});

// Load all foods for selection
async function loadAllFoods() {
    try {
        const data = await window.nutriAI.apiRequest('/api/foods');
        allFoods = data.foods || data || [];
    } catch (error) {
        console.error('Failed to load foods:', error);
    }
}

// Load today's meals from localStorage
function loadTodaysMeals() {
    const saved = localStorage.getItem('todaysMeals');
    if (saved) {
        todaysMeals = JSON.parse(saved);
        renderAllMeals();
    }
}

// Save today's meals to localStorage
function saveTodaysMeals() {
    localStorage.setItem('todaysMeals', JSON.stringify(todaysMeals));
}

// Add food to a meal
async function addFood(mealType) {
    currentMealType = mealType;
    document.getElementById('modalMealType').textContent = mealType;
    
    // Show modal
    document.getElementById('addFoodModal').classList.add('active');
    
    // Display all foods
    displayFoodsInModal(allFoods);
}

// Display foods in modal
function displayFoodsInModal(foods) {
    const grid = document.getElementById('modalFoodsGrid');
    
    if (!foods || foods.length === 0) {
        grid.innerHTML = '<p>No foods available</p>';
        return;
    }
    
    grid.innerHTML = foods.map(food => `
        <div class="food-card-compact" onclick="selectFood(${food.id})">
            <div class="food-info">
                <h4>${food.name}</h4>
                <div class="food-meta">
                    <span><i class="fas fa-fire"></i> ${food.calories || 0} cal</span>
                    <span><i class="fas fa-drumstick-bite"></i> ${food.protein_g || 0}g protein</span>
                </div>
                ${food.health_score ? `
                    <div class="health-badge health-${food.health_score >= 80 ? 'excellent' : food.health_score >= 60 ? 'good' : 'fair'}">
                        ${food.health_score}
                    </div>
                ` : ''}
            </div>
            <button class="btn-sm btn-primary">
                <i class="fas fa-plus"></i>
            </button>
        </div>
    `).join('');
}

// Select food and add to meal
async function selectFood(foodId) {
    const food = allFoods.find(f => f.id === foodId);
    if (!food) return;
    
    // Prompt for quantity
    const quantity = prompt('Enter quantity in grams:', '100');
    if (!quantity || isNaN(quantity)) return;
    
    const qty = parseFloat(quantity);
    
    // Calculate nutrition based on quantity
    const mealItem = {
        id: Date.now(),
        food_id: food.id,
        name: food.name,
        quantity: qty,
        calories: Math.round((food.calories || 0) * qty / 100),
        protein: Math.round((food.protein_g || 0) * qty / 100),
        carbs: Math.round((food.carbs_g || 0) * qty / 100),
        fat: Math.round((food.fat_g || 0) * qty / 100)
    };
    
    // Add to current meal type
    todaysMeals[currentMealType].push(mealItem);
    saveTodaysMeals();
    renderMeal(currentMealType);
    updateDailySummary();
    
    closeModal('addFoodModal');
    window.nutriAI.showToast(`${food.name} added to ${currentMealType}`, 'success');
}

// Render all meals
function renderAllMeals() {
    renderMeal('Breakfast');
    renderMeal('Lunch');
    renderMeal('Dinner');
    renderMeal('Snack');
    updateDailySummary();
}

// Render a specific meal section
function renderMeal(mealType) {
    const container = document.getElementById(`${mealType.toLowerCase()}Items`);
    const items = todaysMeals[mealType];
    
    if (!items || items.length === 0) {
        container.innerHTML = `
            <div class="empty-meal">
                <i class="fas fa-utensils"></i>
                <p>No items added yet</p>
            </div>
        `;
        document.getElementById(`${mealType.toLowerCase()}Calories`).textContent = '0 cal';
        return;
    }
    
    const totalCals = items.reduce((sum, item) => sum + item.calories, 0);
    document.getElementById(`${mealType.toLowerCase()}Calories`).textContent = `${totalCals} cal`;
    
    container.innerHTML = items.map(item => `
        <div class="meal-item-card">
            <div class="meal-item-info">
                <h4>${item.name}</h4>
                <p>${item.quantity}g • ${item.calories} cal</p>
                <div class="meal-item-macros">
                    <span>P: ${item.protein}g</span>
                    <span>C: ${item.carbs}g</span>
                    <span>F: ${item.fat}g</span>
                </div>
            </div>
            <div class="meal-item-actions">
                <button class="btn-icon" onclick="removeFood('${mealType}', ${item.id})" title="Remove">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Remove food from meal
function removeFood(mealType, itemId) {
    todaysMeals[mealType] = todaysMeals[mealType].filter(item => item.id !== itemId);
    saveTodaysMeals();
    renderMeal(mealType);
    updateDailySummary();
    window.nutriAI.showToast('Item removed', 'success');
}

// Update daily summary
function updateDailySummary() {
    let totalCalories = 0;
    let totalProtein = 0;
    let totalCarbs = 0;
    let totalFat = 0;
    
    Object.values(todaysMeals).forEach(meals => {
        meals.forEach(item => {
            totalCalories += item.calories;
            totalProtein += item.protein;
            totalCarbs += item.carbs;
            totalFat += item.fat;
        });
    });
    
    document.getElementById('totalCalories').textContent = totalCalories;
    document.getElementById('totalProtein').textContent = totalProtein + 'g';
    document.getElementById('totalCarbs').textContent = totalCarbs + 'g';
    document.getElementById('totalFat').textContent = totalFat + 'g';
}

// Filter foods based on search and filter
function filterFoods() {
    const searchTerm = document.getElementById('foodSearchInput').value.toLowerCase();
    
    let filtered = allFoods.filter(food => 
        food.name.toLowerCase().includes(searchTerm)
    );
    
    // Apply current filter
    filtered = applyFilterToFoods(filtered, currentFilter);
    
    displayFoodsInModal(filtered);
}

// Apply filter
function applyFilter(filterType) {
    currentFilter = filterType;
    
    // Update active filter chip
    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.classList.remove('active');
    });
    event.target.classList.add('active');
    
    let filtered = [...allFoods];
    filtered = applyFilterToFoods(filtered, filterType);
    
    displayFoodsInModal(filtered);
}

// Apply filter logic
function applyFilterToFoods(foods, filterType) {
    switch(filterType) {
        case 'high-protein':
            return foods.filter(f => (f.protein_g || 0) >= 15);
        case 'low-carb':
            return foods.filter(f => (f.carbs_g || 0) <= 15);
        case 'low-calorie':
            return foods.filter(f => (f.calories || 0) <= 100);
        case 'healthy':
            return foods.filter(f => (f.health_score || 0) >= 70);
        default:
            return foods;
    }
}

// Show generate modal
function showGenerateModal() {
    document.getElementById('generatePlanModal').classList.add('active');
}

// Setup generate plan form
function setupGeneratePlanForm() {
    const form = document.getElementById('generatePlanForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            diet_type: formData.get('diet_type'),
            budget_per_day: parseFloat(formData.get('budget_per_day'))
        };
        
        try {
            window.nutriAI.showToast('Generating meal plan...', 'info');
            const result = await window.nutriAI.apiRequest('/api/meal-plans', 'POST', data);
            
            closeModal('generatePlanModal');
            window.nutriAI.showToast('7-day meal plan generated!', 'success');
            
            // Load and display the plan
            if (result.plan_id) {
                await viewWeeklyPlan(result.plan_id);
            }
        } catch (error) {
            console.error('Failed to generate plan:', error);
        }
    });
}

// View weekly plan
async function viewWeeklyPlan(planId) {
    try {
        const plan = await window.nutriAI.apiRequest(`/api/meal-plans/${planId}`);
        displayWeeklyPlan(plan);
        document.getElementById('weeklyPlanModal').classList.add('active');
    } catch (error) {
        console.error('Failed to load plan:', error);
    }
}

// Display weekly plan
function displayWeeklyPlan(plan) {
    document.getElementById('weeklyPlanTitle').textContent = plan.name;
    
    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    
    const html = days.map((day, index) => {
        const dayData = plan[day] || {};
        
        return `
            <div class="day-card">
                <h3>${dayNames[index]}</h3>
                <button class="btn btn-sm" onclick="loadDayMeals('${day}', ${plan.id})">
                    <i class="fas fa-calendar-check"></i> Use Today
                </button>
                ${['Breakfast', 'Lunch', 'Dinner', 'Snack'].map(meal => {
                    const items = dayData[meal] || [];
                    return `
                        <div class="day-meal">
                            <h4>${meal}</h4>
                            ${items.length > 0 ? items.map(item => `
                                <div class="day-meal-item">
                                    <span>${item.name}</span>
                                    <span>${item.calories} cal</span>
                                </div>
                            `).join('') : '<p>No items</p>'}
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }).join('');
    
    document.getElementById('weeklyMeals').innerHTML = html;
}

// Load day's meals into today's planner
async function loadDayMeals(day, planId) {
    try {
        const plan = await window.nutriAI.apiRequest(`/api/meal-plans/${planId}`);
        const dayData = plan[day] || {};
        
        // Clear current meals
        todaysMeals = {
            Breakfast: [],
            Lunch: [],
            Dinner: [],
            Snack: []
        };
        
        // Load meals from the plan
        ['Breakfast', 'Lunch', 'Dinner', 'Snack'].forEach(mealType => {
            const items = dayData[mealType] || [];
            todaysMeals[mealType] = items.map(item => ({
                id: Date.now() + Math.random(),
                name: item.name,
                quantity: item.quantity || 100,
                calories: item.calories || 0,
                protein: item.protein || 0,
                carbs: item.carbs || 0,
                fat: item.fat || 0
            }));
        });
        
        saveTodaysMeals();
        renderAllMeals();
        closeModal('weeklyPlanModal');
        
        window.nutriAI.showToast(`${day.charAt(0).toUpperCase() + day.slice(1)}'s meals loaded!`, 'success');
    } catch (error) {
        console.error('Failed to load day meals:', error);
    }
}

// Show saved plans
async function showSavedPlans() {
    document.getElementById('savedPlansModal').classList.add('active');
    
    try {
        const plans = await window.nutriAI.apiRequest('/api/meal-plans');
        displaySavedPlans(plans);
    } catch (error) {
        console.error('Failed to load saved plans:', error);
    }
}

// Display saved plans
function displaySavedPlans(plans) {
    const container = document.getElementById('savedPlansList');
    
    if (!plans || plans.length === 0) {
        container.innerHTML = '<p>No saved plans yet</p>';
        return;
    }
    
    container.innerHTML = plans.map(plan => `
        <div class="plan-card">
            <h4>${plan.name}</h4>
            <p>${new Date(plan.week_start_date).toLocaleDateString()}</p>
            <div class="plan-stats">
                <span>${plan.total_calories} cal</span>
                <span>${plan.total_protein}g protein</span>
            </div>
            <button class="btn-primary btn-sm" onclick="viewWeeklyPlan(${plan.id})">
                View Plan
            </button>
        </div>
    `).join('');
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// Add CSS
const mealPlannerStyles = document.createElement('style');
mealPlannerStyles.textContent = `
    .meals-sections {
        display: grid;
        gap: 24px;
        margin-bottom: 24px;
    }
    
    .meal-section {
        background: white;
        border-radius: var(--border-radius-lg);
        padding: 24px;
        box-shadow: var(--shadow-sm);
    }
    
    .meal-section-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 20px;
    }
    
    .meal-icon {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .meal-icon.breakfast { background: linear-gradient(135deg, #ff9a9e, #fad0c4); }
    .meal-icon.lunch { background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
    .meal-icon.dinner { background: linear-gradient(135deg, #ffecd2, #fcb69f); }
    .meal-icon.snack { background: linear-gradient(135deg, #84fab0, #8fd3f4); }
    
    .meal-section-header h3 {
        margin: 0 0 4px 0;
        flex: 1;
    }
    
    .meal-calories {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .btn-add {
        padding: 10px 20px;
        background: var(--primary);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        transition: var(--transition);
    }
    
    .btn-add:hover {
        background: var(--primary-dark);
        transform: translateY(-2px);
    }
    
    .meal-items {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .empty-meal {
        text-align: center;
        padding: 40px;
        color: var(--text-secondary);
    }
    
    .empty-meal i {
        font-size: 3rem;
        margin-bottom: 12px;
        opacity: 0.3;
    }
    
    .meal-item-card {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px;
        background: var(--bg-secondary);
        border-radius: var(--border-radius);
        transition: var(--transition);
    }
    
    .meal-item-card:hover {
        box-shadow: var(--shadow-sm);
    }
    
    .meal-item-info {
        flex: 1;
    }
    
    .meal-item-info h4 {
        margin: 0 0 4px 0;
        font-size: 1rem;
    }
    
    .meal-item-info p {
        margin: 0 0 8px 0;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .meal-item-macros {
        display: flex;
        gap: 16px;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .meal-item-actions {
        display: flex;
        gap: 8px;
    }
    
    .btn-icon {
        width: 36px;
        height: 36px;
        padding: 0;
        background: transparent;
        border: 1px solid var(--gray-300);
        border-radius: 8px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: var(--transition);
    }
    
    .btn-icon:hover {
        background: var(--red);
        color: white;
        border-color: var(--red);
    }
    
    .daily-summary {
        margin-top: 24px;
    }
    
    .summary-stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
    }
    
    .summary-stat {
        text-align: center;
    }
    
    .summary-stat .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 8px;
    }
    
    .summary-stat .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    .search-filters {
        margin-bottom: 24px;
    }
    
    .search-input {
        width: 100%;
        padding: 12px 16px;
        border: 1px solid var(--gray-300);
        border-radius: var(--border-radius);
        font-size: 1rem;
        margin-bottom: 16px;
    }
    
    .filter-chips {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    
    .filter-chip {
        padding: 8px 16px;
        background: var(--bg-secondary);
        border: 1px solid var(--gray-300);
        border-radius: 20px;
        cursor: pointer;
        transition: var(--transition);
        font-size: 0.9rem;
    }
    
    .filter-chip:hover,
    .filter-chip.active {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }
    
    .foods-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 16px;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .food-card-compact {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--border-radius);
        cursor: pointer;
        transition: var(--transition);
    }
    
    .food-card-compact:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    .food-info {
        flex: 1;
    }
    
    .food-info h4 {
        margin: 0 0 8px 0;
        font-size: 0.95rem;
    }
    
    .food-meta {
        display: flex;
        gap: 12px;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    
    .weekly-view {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
    }
    
    .day-card {
        background: var(--bg-secondary);
        padding: 16px;
        border-radius: var(--border-radius);
    }
    
    .day-card h3 {
        margin: 0 0 16px 0;
        font-size: 1.1rem;
        color: var(--primary);
    }
    
    .day-meal {
        margin-bottom: 16px;
    }
    
    .day-meal h4 {
        margin: 0 0 8px 0;
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    .day-meal-item {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        font-size: 0.85rem;
        border-bottom: 1px solid var(--gray-200);
    }
    
    .plans-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
    }
    
    .plan-card {
        background: white;
        padding: 20px;
        border-radius: var(--border-radius);
        border: 1px solid var(--gray-200);
    }
    
    .plan-card h4 {
        margin: 0 0 8px 0;
    }
    
    .plan-stats {
        display: flex;
        gap: 16px;
        margin: 12px 0;
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    .modal-xlarge {
        max-width: 1200px;
    }
    
    .top-bar-actions {
        display: flex;
        gap: 12px;
    }
    
    @media (max-width: 768px) {
        .summary-stats {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .weekly-view {
            grid-template-columns: 1fr;
        }
    }
`;
document.head.appendChild(mealPlannerStyles);
