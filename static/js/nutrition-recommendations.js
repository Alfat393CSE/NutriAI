// Nutrition Recommendations JavaScript

let currentRecommendations = null;

// Load recommendations on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadRecommendations();
    setupQuickCalculator();
});

// Load nutrition recommendations
async function loadRecommendations() {
    try {
        showLoading();
        
        const response = await fetch('/api/nutrition-recommendations');
        
        if (!response.ok) {
            throw new Error('Failed to load recommendations');
        }
        
        const data = await response.json();
        currentRecommendations = data;
        
        // Display all sections
        displayProfileSummary(data.user_profile);
        displayCalorieTarget(data.calorie_target);
        displayMacros(data.macros);
        displayBMI(data.user_profile);
        displayTopFoods(data.top_recommended_foods);
        displayFoodsToAvoid(data.foods_to_avoid);
        displayMealSuggestions(data.meal_suggestions);
        displayMealDistribution(data.meal_distribution);
        
        hideLoading();
        
    } catch (error) {
        console.error('Error loading recommendations:', error);
        hideLoading();
        showError('Failed to load recommendations. Please try again.');
    }
}

// Display profile summary
function displayProfileSummary(profile) {
    const html = `
        <div class="profile-stat">
            <i class="fas fa-birthday-cake"></i>
            <div>
                <strong>Age</strong>
                <span>${profile.age || 'N/A'} years</span>
            </div>
        </div>
        <div class="profile-stat">
            <i class="fas fa-venus-mars"></i>
            <div>
                <strong>Gender</strong>
                <span>${profile.gender ? profile.gender.charAt(0).toUpperCase() + profile.gender.slice(1) : 'N/A'}</span>
            </div>
        </div>
        <div class="profile-stat">
            <i class="fas fa-weight"></i>
            <div>
                <strong>Weight</strong>
                <span>${profile.weight_kg || 'N/A'} kg</span>
            </div>
        </div>
        <div class="profile-stat">
            <i class="fas fa-ruler-vertical"></i>
            <div>
                <strong>Height</strong>
                <span>${profile.height_cm || 'N/A'} cm</span>
            </div>
        </div>
        <div class="profile-stat">
            <i class="fas fa-running"></i>
            <div>
                <strong>Activity</strong>
                <span>${formatActivityLevel(profile.activity_level)}</span>
            </div>
        </div>
        <div class="profile-stat">
            <i class="fas fa-bullseye"></i>
            <div>
                <strong>Goal</strong>
                <span>${formatGoal(profile.goal)}</span>
            </div>
        </div>
    `;
    
    document.getElementById('profileSummary').innerHTML = html;
    document.getElementById('userGoal').textContent = formatGoal(profile.goal);
}

// Display calorie target
function displayCalorieTarget(calorieInfo) {
    document.getElementById('calorieTarget').textContent = calorieInfo.target_calories.toLocaleString();
    document.getElementById('bmr').textContent = calorieInfo.bmr.toLocaleString();
    document.getElementById('tdee').textContent = calorieInfo.tdee.toLocaleString();
}

// Display macros
function displayMacros(macros) {
    const html = `
        <div class="macro-item protein">
            <div class="macro-label">
                <i class="fas fa-drumstick-bite"></i> Protein
            </div>
            <div class="macro-value">${macros.protein_g}g</div>
            <div class="macro-percentage">${macros.protein_percentage}%</div>
            <div class="progress-bar">
                <div class="progress-fill protein-fill" style="width: ${macros.protein_percentage}%"></div>
            </div>
        </div>
        <div class="macro-item carbs">
            <div class="macro-label">
                <i class="fas fa-bread-slice"></i> Carbs
            </div>
            <div class="macro-value">${macros.carbs_g}g</div>
            <div class="macro-percentage">${macros.carbs_percentage}%</div>
            <div class="progress-bar">
                <div class="progress-fill carbs-fill" style="width: ${macros.carbs_percentage}%"></div>
            </div>
        </div>
        <div class="macro-item fats">
            <div class="macro-label">
                <i class="fas fa-bacon"></i> Fats
            </div>
            <div class="macro-value">${macros.fat_g}g</div>
            <div class="macro-percentage">${macros.fat_percentage}%</div>
            <div class="progress-bar">
                <div class="progress-fill fats-fill" style="width: ${macros.fat_percentage}%"></div>
            </div>
        </div>
    `;
    
    document.getElementById('macroBreakdown').innerHTML = html;
}

// Display BMI
function displayBMI(profile) {
    document.getElementById('bmiValue').textContent = profile.bmi || '--';
    document.getElementById('bmiCategory').textContent = profile.bmi_category || '--';
    document.getElementById('bmiAdvice').textContent = profile.bmi_advice || '--';
    
    // Color code BMI card
    const bmiCard = document.querySelector('.bmi-card');
    const bmi = profile.bmi;
    if (bmi < 18.5) {
        bmiCard.classList.add('underweight');
    } else if (bmi < 25) {
        bmiCard.classList.add('normal');
    } else if (bmi < 30) {
        bmiCard.classList.add('overweight');
    } else {
        bmiCard.classList.add('obese');
    }
}

// Display top recommended foods
function displayTopFoods(foods) {
    const html = foods.map(item => `
        <div class="food-card recommended">
            <div class="food-card-header">
                <h4>${item.food.name}</h4>
                <span class="fit-badge">${item.fit_percentage}% Match</span>
            </div>
            <div class="food-category">
                <i class="fas fa-tag"></i> ${item.food.category}
            </div>
            <div class="food-nutrients">
                <div class="nutrient">
                    <i class="fas fa-fire"></i>
                    <span>${item.food.calories} cal</span>
                </div>
                <div class="nutrient">
                    <i class="fas fa-drumstick-bite"></i>
                    <span>${item.food.protein_g}g protein</span>
                </div>
                <div class="nutrient">
                    <i class="fas fa-bread-slice"></i>
                    <span>${item.food.carbs_g}g carbs</span>
                </div>
                <div class="nutrient">
                    <i class="fas fa-bacon"></i>
                    <span>${item.food.fat_g}g fat</span>
                </div>
            </div>
            <div class="food-health-score">
                <div class="health-rating ${item.food.health_rating.toLowerCase()}">${item.food.health_rating}</div>
                <span class="health-score">Health Score: ${item.food.health_score}/100</span>
            </div>
            <button class="btn-secondary btn-sm" onclick="viewFoodDetails(${item.food.id})">
                <i class="fas fa-info-circle"></i> View Details
            </button>
        </div>
    `).join('');
    
    document.getElementById('topFoods').innerHTML = html;
}

// Display foods to avoid
function displayFoodsToAvoid(foods) {
    if (foods.length === 0) {
        document.getElementById('avoidFoods').innerHTML = '<p class="no-data">No specific foods to avoid based on your profile.</p>';
        return;
    }
    
    const html = foods.map(item => `
        <div class="avoid-item">
            <div class="avoid-icon">
                <i class="fas fa-ban"></i>
            </div>
            <div class="avoid-content">
                <h4>${item.item}</h4>
                <p>${item.reason}</p>
            </div>
        </div>
    `).join('');
    
    document.getElementById('avoidFoods').innerHTML = html;
}

// Display meal suggestions
function displayMealSuggestions(suggestions) {
    displayMealItems('breakfastSuggestions', suggestions.breakfast);
    displayMealItems('lunchSuggestions', suggestions.lunch);
    displayMealItems('dinnerSuggestions', suggestions.dinner);
    displayMealItems('snackSuggestions', suggestions.snacks);
}

function displayMealItems(elementId, foods) {
    if (foods.length === 0) {
        document.getElementById(elementId).innerHTML = '<p class="no-data">No suggestions available</p>';
        return;
    }
    
    const html = foods.map(food => `
        <div class="meal-item">
            <strong>${food.name}</strong>
            <div class="meal-item-nutrients">
                <span><i class="fas fa-fire"></i> ${food.calories} cal</span>
                <span><i class="fas fa-drumstick-bite"></i> ${food.protein_g}g P</span>
            </div>
        </div>
    `).join('');
    
    document.getElementById(elementId).innerHTML = html;
}

// Display meal distribution
function displayMealDistribution(distribution) {
    const total = Object.values(distribution).reduce((a, b) => a + b, 0);
    
    const html = `
        <div class="distribution-grid">
            <div class="distribution-item">
                <div class="distribution-icon breakfast">
                    <i class="fas fa-coffee"></i>
                </div>
                <h4>Breakfast</h4>
                <div class="distribution-calories">${distribution.breakfast} cal</div>
                <div class="distribution-percentage">${Math.round((distribution.breakfast / total) * 100)}%</div>
            </div>
            <div class="distribution-item">
                <div class="distribution-icon lunch">
                    <i class="fas fa-hamburger"></i>
                </div>
                <h4>Lunch</h4>
                <div class="distribution-calories">${distribution.lunch} cal</div>
                <div class="distribution-percentage">${Math.round((distribution.lunch / total) * 100)}%</div>
            </div>
            <div class="distribution-item">
                <div class="distribution-icon dinner">
                    <i class="fas fa-pizza-slice"></i>
                </div>
                <h4>Dinner</h4>
                <div class="distribution-calories">${distribution.dinner} cal</div>
                <div class="distribution-percentage">${Math.round((distribution.dinner / total) * 100)}%</div>
            </div>
            <div class="distribution-item">
                <div class="distribution-icon snacks">
                    <i class="fas fa-cookie-bite"></i>
                </div>
                <h4>Snacks</h4>
                <div class="distribution-calories">${distribution.snacks} cal</div>
                <div class="distribution-percentage">${Math.round((distribution.snacks / total) * 100)}%</div>
            </div>
        </div>
    `;
    
    document.getElementById('mealDistribution').innerHTML = html;
}

// Setup quick calculator
function setupQuickCalculator() {
    const form = document.getElementById('quickCalculator');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = {
            age: parseInt(formData.get('age')),
            gender: formData.get('gender'),
            weight_kg: parseFloat(formData.get('weight_kg')),
            height_cm: parseFloat(formData.get('height_cm')),
            activity_level: formData.get('activity_level'),
            goal: formData.get('goal')
        };
        
        try {
            showLoading('Calculating...');
            
            const response = await fetch('/api/calculate-nutrition-targets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error('Calculation failed');
            }
            
            const result = await response.json();
            displayCalculatorResult(result);
            hideLoading();
            
        } catch (error) {
            console.error('Calculator error:', error);
            hideLoading();
            showToast('Calculation failed. Please check your inputs.', 'error');
        }
    });
}

// Display calculator result
function displayCalculatorResult(result) {
    const resultDiv = document.getElementById('calculatorResult');
    
    const html = `
        <h4><i class="fas fa-check-circle"></i> Your Personalized Nutrition Plan</h4>
        <div class="result-grid">
            <div class="result-item">
                <strong>BMI</strong>
                <span>${result.user_profile.bmi}</span>
                <small>${result.user_profile.bmi_category}</small>
            </div>
            <div class="result-item">
                <strong>BMR</strong>
                <span>${result.calorie_target.bmr}</span>
                <small>Base Metabolism</small>
            </div>
            <div class="result-item">
                <strong>TDEE</strong>
                <span>${result.calorie_target.tdee}</span>
                <small>Daily Energy</small>
            </div>
            <div class="result-item">
                <strong>Target Calories</strong>
                <span>${result.calorie_target.target_calories}</span>
                <small>Per Day</small>
            </div>
            <div class="result-item">
                <strong>Protein</strong>
                <span>${result.macros.protein_g}g</span>
                <small>${result.macros.protein_percentage}%</small>
            </div>
            <div class="result-item">
                <strong>Carbs</strong>
                <span>${result.macros.carbs_g}g</span>
                <small>${result.macros.carbs_percentage}%</small>
            </div>
            <div class="result-item">
                <strong>Fats</strong>
                <span>${result.macros.fat_g}g</span>
                <small>${result.macros.fat_percentage}%</small>
            </div>
        </div>
        <div style="padding: 1.5rem; background: rgba(99, 102, 241, 0.1); border-radius: 12px; border-left: 4px solid var(--primary); margin-top: 1rem;">
            <p style="margin: 0; color: var(--text-primary); font-weight: 500; display: flex; align-items: center; gap: 0.75rem;">
                <i class="fas fa-lightbulb" style="color: var(--primary); font-size: 1.25rem;"></i>
                ${result.user_profile.bmi_advice}
            </p>
        </div>
    `;
    
    resultDiv.innerHTML = html;
    resultDiv.classList.add('show');
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Refresh recommendations
async function refreshRecommendations() {
    await loadRecommendations();
    showToast('Recommendations refreshed!', 'success');
}

// View food details
function viewFoodDetails(foodId) {
    window.location.href = `/food-search?food=${foodId}`;
}

// Show loading
function showLoading(message = 'Loading...') {
    const loadingState = document.getElementById('loadingState');
    const content = document.getElementById('recommendationsContent');
    
    if (loadingState) {
        loadingState.querySelector('p').textContent = message;
        loadingState.style.display = 'flex';
    }
    
    if (content) {
        content.style.display = 'none';
    }
}

// Hide loading
function hideLoading() {
    const loadingState = document.getElementById('loadingState');
    const content = document.getElementById('recommendationsContent');
    
    if (loadingState) {
        loadingState.style.display = 'none';
    }
    
    if (content) {
        content.style.display = 'block';
    }
}

// Show error
function showError(message) {
    const content = document.getElementById('recommendationsContent');
    content.innerHTML = `
        <div class="error-state">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Oops! Something went wrong</h3>
            <p>${message}</p>
            <button class="btn-primary" onclick="loadRecommendations()">
                <i class="fas fa-redo"></i> Try Again
            </button>
        </div>
    `;
    content.style.display = 'block';
}

// Format activity level
function formatActivityLevel(level) {
    const levels = {
        'sedentary': 'Sedentary',
        'light': 'Light Activity',
        'moderate': 'Moderate Activity',
        'active': 'Active',
        'very_active': 'Very Active'
    };
    return levels[level] || level;
}

// Format goal
function formatGoal(goal) {
    if (!goal) return 'Not Set';
    return goal.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}
