// Food Search JavaScript

let allFoods = [];

document.addEventListener('DOMContentLoaded', async () => {
    await loadFoods();
});

async function loadFoods() {
    try {
        const data = await window.nutriAI.apiRequest('/api/foods');
        allFoods = data.foods || data || [];
        displayFoods(allFoods);
    } catch (error) {
        document.getElementById('foodsGrid').innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-circle"></i>
                <p>Failed to load foods</p>
            </div>
        `;
    }
}

function displayFoods(foods) {
    const grid = document.getElementById('foodsGrid');
    
    if (foods.length === 0) {
        grid.innerHTML = '<div class="empty-state"><p>No foods found</p></div>';
        return;
    }
    
    grid.innerHTML = foods.map(food => `
        <div class="food-card" onclick="showFoodDetail(${food.id})">
            <div class="food-card-header">
                <div class="food-icon ${getHealthClass(food.health_rating)}">
                    <i class="fas fa-${getCategoryIcon(food.category)}"></i>
                </div>
                <span class="health-badge ${getHealthClass(food.health_rating)}">
                    ${food.health_rating || 'N/A'}
                </span>
            </div>
            <h3 class="food-name">${food.name}</h3>
            <p class="food-category">${food.category || 'Uncategorized'}</p>
            <div class="food-nutrition">
                <div class="nutrition-item">
                    <span class="nutrition-label">Calories</span>
                    <span class="nutrition-value">${food.calories || 0}</span>
                </div>
                <div class="nutrition-item">
                    <span class="nutrition-label">Protein</span>
                    <span class="nutrition-value">${food.protein_g || 0}g</span>
                </div>
            </div>
            <div class="food-actions">
                <button class="btn-sm btn-primary" onclick="event.stopPropagation(); logThisFood(${food.id})">
                    <i class="fas fa-plus"></i> Log
                </button>
                <button class="btn-sm btn-outline" onclick="event.stopPropagation(); findAlternatives(${food.id})">
                    <i class="fas fa-exchange-alt"></i> Swap
                </button>
            </div>
        </div>
    `).join('');
}

function getHealthClass(rating) {
    const classes = {
        'Excellent': 'health-excellent',
        'Good': 'health-good',
        'Fair': 'health-fair',
        'Unhealthy': 'health-poor'
    };
    return classes[rating] || 'health-good';
}

function getCategoryIcon(category) {
    const icons = {
        'Proteins': 'drumstick-bite',
        'Vegetables': 'leaf',
        'Fruits': 'apple-alt',
        'Grains': 'bread-slice',
        'Dairy': 'cheese',
        'Nuts': 'seedling',
        'Legumes': 'seedling',
        'Beverages': 'mug-hot'
    };
    return icons[category] || 'utensils';
}

function searchFoods() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allFoods.filter(food => 
        food.name.toLowerCase().includes(query)
    );
    displayFoods(filtered);
}

function filterFoods() {
    const category = document.getElementById('categoryFilter').value;
    const health = document.getElementById('healthFilter').value;
    
    let filtered = allFoods;
    
    if (category) {
        filtered = filtered.filter(f => f.category === category);
    }
    
    if (health) {
        filtered = filtered.filter(f => f.health_rating === health);
    }
    
    const query = document.getElementById('searchInput').value.toLowerCase();
    if (query) {
        filtered = filtered.filter(f => f.name.toLowerCase().includes(query));
    }
    
    displayFoods(filtered);
}

async function showFoodDetail(foodId) {
    try {
        const food = await window.nutriAI.apiRequest(`/api/foods/${foodId}`);
        
        // Check for risks and warnings
        const riskCheck = await window.nutriAI.apiRequest(`/api/foods/${foodId}/check-risks`);
        
        const modal = document.getElementById('foodDetailModal');
        
        document.getElementById('foodName').textContent = food.name;
        
        // Build risk alerts section
        let alertsHtml = '';
        if (riskCheck.has_risks || riskCheck.has_warnings) {
            alertsHtml = '<div class="risk-alerts-section">';
            
            // Show critical risks first
            if (riskCheck.risks && riskCheck.risks.length > 0) {
                riskCheck.risks.forEach(risk => {
                    alertsHtml += `
                        <div class="alert alert-danger">
                            <i class="fas fa-${risk.icon}"></i>
                            <span>${risk.message}</span>
                        </div>
                    `;
                });
            }
            
            // Show warnings
            if (riskCheck.warnings && riskCheck.warnings.length > 0) {
                riskCheck.warnings.forEach(warning => {
                    const alertClass = warning.severity === 'warning' ? 'alert-warning' : 'alert-info';
                    alertsHtml += `
                        <div class="alert ${alertClass}">
                            <i class="fas fa-${warning.icon}"></i>
                            <span>${warning.message}</span>
                        </div>
                    `;
                });
            }
            
            alertsHtml += '</div>';
        } else {
            alertsHtml = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i>
                    <span>✓ Safe for your profile - No known risks detected</span>
                </div>
            `;
        }
        
        document.getElementById('foodDetailBody').innerHTML = `
            ${alertsHtml}
            
            <div class="food-detail-grid">
                <div class="detail-section">
                    <h4>Macronutrients (per 100g)</h4>
                    <div class="nutrition-table">
                        <div class="nutrition-row">
                            <span>Calories</span>
                            <strong>${food.calories || 0} kcal</strong>
                        </div>
                        <div class="nutrition-row">
                            <span>Protein</span>
                            <strong>${food.protein_g || 0}g</strong>
                        </div>
                        <div class="nutrition-row">
                            <span>Carbohydrates</span>
                            <strong>${food.carbs_g || 0}g</strong>
                        </div>
                        <div class="nutrition-row">
                            <span>Fat</span>
                            <strong>${food.fat_g || 0}g</strong>
                        </div>
                        <div class="nutrition-row">
                            <span>Fiber</span>
                            <strong>${food.fiber_g || 0}g</strong>
                        </div>
                    </div>
                </div>
                <div class="detail-section">
                    <h4>Additional Info</h4>
                    <div class="info-items">
                        <div class="info-item">
                            <i class="fas fa-trophy"></i>
                            <div>
                                <span>Health Score</span>
                                <strong>${food.health_score || 'N/A'}/100</strong>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-star"></i>
                            <div>
                                <span>Rating</span>
                                <strong>${food.health_rating || 'N/A'}</strong>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-tag"></i>
                            <div>
                                <span>Category</span>
                                <strong>${food.category || 'N/A'}</strong>
                            </div>
                        </div>
                        ${food.common_allergens ? `
                        <div class="info-item warning">
                            <i class="fas fa-exclamation-triangle"></i>
                            <div>
                                <span>Allergens</span>
                                <strong>${food.common_allergens}</strong>
                            </div>
                        </div>
                        ` : ''}
                    </div>
                </div>
            </div>
            <div class="modal-actions">
                <button class="btn-primary" onclick="logThisFood(${food.id}); closeModal('foodDetailModal')">
                    <i class="fas fa-plus"></i> Log This Food
                </button>
                <button class="btn-secondary" onclick="findAlternatives(${food.id})">
                    <i class="fas fa-exchange-alt"></i> Find Alternatives
                </button>
            </div>
        `;
        
        modal.classList.add('active');
    } catch (error) {
        console.error('Failed to load food details:', error);
    }
}

async function logThisFood(foodId) {
    const quantity = prompt('Enter quantity in grams:', '100');
    if (!quantity) return;
    
    const mealType = prompt('Meal type? (Breakfast/Lunch/Dinner/Snack)', 'Snack');
    
    try {
        await window.nutriAI.apiRequest('/api/food-logs', 'POST', {
            food_id: foodId,
            quantity_g: parseFloat(quantity),
            meal_type: mealType,
            date: new Date().toISOString().split('T')[0]
        });
        
        window.nutriAI.showToast('Food logged successfully!', 'success');
    } catch (error) {
        // Error handled by apiRequest
    }
}

async function findAlternatives(foodId) {
    try {
        const alternatives = await window.nutriAI.apiRequest(`/api/foods/alternatives/${foodId}`);
        
        if (alternatives.length === 0) {
            window.nutriAI.showToast('No alternatives found', 'info');
            return;
        }
        
        const names = alternatives.map(a => a.food ? a.food.name : a.name).join(', ');
        window.nutriAI.showToast(`Try these: ${names}`, 'success');
    } catch (error) {
        // Error handled
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Add CSS for food cards
const foodSearchStyles = document.createElement('style');
foodSearchStyles.textContent = `
    .search-section {
        margin-bottom: 32px;
        display: flex;
        gap: 16px;
        align-items: center;
    }
    .search-box {
        flex: 1;
        position: relative;
        display: flex;
        align-items: center;
    }
    .search-box i {
        position: absolute;
        left: 16px;
        color: var(--text-secondary);
    }
    .search-box input {
        width: 100%;
        padding: 14px 16px 14px 48px;
        border: 2px solid var(--gray-200);
        border-radius: var(--border-radius);
        font-size: 1rem;
    }
    .filters {
        display: flex;
        gap: 12px;
    }
    .foods-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 24px;
    }
    .food-card {
        background: white;
        border-radius: var(--border-radius-lg);
        padding: 24px;
        box-shadow: var(--shadow-md);
        cursor: pointer;
        transition: var(--transition);
    }
    .food-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    .food-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 16px;
    }
    .food-icon {
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: var(--border-radius);
        font-size: 1.5rem;
        color: white;
    }
    .food-icon.health-excellent { background: linear-gradient(135deg, #22c55e, #16a34a); }
    .food-icon.health-good { background: linear-gradient(135deg, #3b82f6, #2563eb); }
    .food-icon.health-fair { background: linear-gradient(135deg, #f97316, #ea580c); }
    .food-icon.health-poor { background: linear-gradient(135deg, #ef4444, #dc2626); }
    .health-badge {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
    }
    .health-badge.health-excellent { background: #22c55e; }
    .health-badge.health-good { background: #3b82f6; }
    .health-badge.health-fair { background: #f97316; }
    .health-badge.health-poor { background: #ef4444; }
    .food-name {
        font-size: 1.25rem;
        margin-bottom: 4px;
    }
    .food-category {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin-bottom: 16px;
    }
    .food-nutrition {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        padding: 16px 0;
        border-top: 1px solid var(--gray-200);
        border-bottom: 1px solid var(--gray-200);
        margin-bottom: 16px;
    }
    .nutrition-item {
        text-align: center;
    }
    .nutrition-label {
        display: block;
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-bottom: 4px;
    }
    .nutrition-value {
        display: block;
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--primary);
    }
    .food-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    .food-detail-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 32px;
        margin-bottom: 24px;
    }
    .detail-section h4 {
        margin-bottom: 16px;
    }
    .nutrition-table {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .nutrition-row {
        display: flex;
        justify-content: space-between;
        padding: 12px;
        background: var(--bg-secondary);
        border-radius: 8px;
    }
    .info-items {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .info-item {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 12px;
        background: var(--bg-secondary);
        border-radius: 8px;
    }
    .info-item i {
        font-size: 1.5rem;
        color: var(--primary);
    }
    .info-item.warning i {
        color: var(--orange);
    }
    .info-item div {
        display: flex;
        flex-direction: column;
    }
    .info-item span {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    .modal-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    .modal-large {
        max-width: 900px;
    }
`;
document.head.appendChild(foodSearchStyles);
