// Food Comparison Page JavaScript
let allFoods = [];
let selectedFood1 = null;
let selectedFood2 = null;
let macroChart1 = null;
let macroChart2 = null;
let comparisonChart = null;
let differenceChart = null;

// Initialize page
document.addEventListener('DOMContentLoaded', async () => {
    await loadFoods();
});

// Load all foods
async function loadFoods() {
    try {
        console.log('Loading foods...');
        const data = await window.nutriAI.apiRequest('/api/foods');
        allFoods = data.foods || [];
        console.log('Loaded foods:', allFoods.length);
        
        // Populate both dropdowns
        const food1Select = document.getElementById('food1Select');
        const food2Select = document.getElementById('food2Select');
        
        if (!food1Select || !food2Select) {
            console.error('Dropdown elements not found!');
            return;
        }
        
        allFoods.forEach(food => {
            const option1 = document.createElement('option');
            option1.value = food.id;
            option1.textContent = `${food.name} (${food.category})`;
            food1Select.appendChild(option1);
            
            const option2 = document.createElement('option');
            option2.value = food.id;
            option2.textContent = `${food.name} (${food.category})`;
            food2Select.appendChild(option2);
        });
        
        console.log('Dropdowns populated successfully');
        
    } catch (error) {
        console.error('Error loading foods:', error);
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Failed to load foods', 'error');
        }
    }
}

// Select food
function selectFood(position) {
    console.log('selectFood called for position:', position);
    const selectId = position === 1 ? 'food1Select' : 'food2Select';
    const selectedId = document.getElementById(selectId).value;
    console.log('Selected ID:', selectedId);
    
    if (selectedId) {
        const food = allFoods.find(f => f.id === parseInt(selectedId));
        console.log('Found food:', food);
        if (position === 1) {
            selectedFood1 = food;
        } else {
            selectedFood2 = food;
        }
    }
    
    // If both foods selected, load comparison
    if (selectedFood1 && selectedFood2) {
        loadComparison();
    }
}

// Load comparison
async function loadComparison() {
    try {
        const data = await window.nutriAI.apiRequest(`/api/foods/compare/${selectedFood1.id}/${selectedFood2.id}`);
        
        // Show comparison result, hide empty state
        document.getElementById('comparisonResult').style.display = 'block';
        document.getElementById('emptyState').style.display = 'none';
        
        // Display food cards
        displayFoodCard(1, data.food1);
        displayFoodCard(2, data.food2);
        
        // Display differences
        displayDifferences(data.differences);
        
        // Display health analysis
        displayHealthAnalysis(data.health_analysis);
        
        // Create charts
        createMacroCharts(data.food1, data.food2);
        createComparisonChart(data.food1, data.food2);
        createDifferenceChart(data.differences);
        
    } catch (error) {
        console.error('Error loading comparison:', error);
        window.nutriAI.showToast('Failed to load comparison', 'error');
    }
}

// Display food card
function displayFoodCard(position, food) {
    const prefix = `food${position}`;
    
    document.getElementById(`${prefix}Name`).textContent = food.name;
    document.getElementById(`${prefix}Calories`).textContent = `${food.calories || 0} kcal`;
    document.getElementById(`${prefix}Protein`).textContent = `${food.protein_g || 0}g`;
    document.getElementById(`${prefix}Carbs`).textContent = `${food.carbs_g || 0}g`;
    document.getElementById(`${prefix}Fat`).textContent = `${food.fat_g || 0}g`;
    document.getElementById(`${prefix}Fiber`).textContent = `${food.fiber_g || 0}g`;
    document.getElementById(`${prefix}Sugar`).textContent = `${food.sugar_g || 0}g`;
    document.getElementById(`${prefix}Sodium`).textContent = `${food.sodium_mg || 0}mg`;
    
    // Health score
    const healthScore = food.health_score || 0;
    const healthEl = document.getElementById(`${prefix}Health`);
    let healthClass = 'excellent';
    if (healthScore < 50) healthClass = 'poor';
    else if (healthScore < 70) healthClass = 'fair';
    else if (healthScore < 85) healthClass = 'good';
    
    healthEl.className = `health-score ${healthClass}`;
    healthEl.innerHTML = `<i class="fas fa-heart"></i> ${healthScore}%`;
    
    // Tags
    const tagsEl = document.getElementById(`${prefix}Tags`);
    tagsEl.innerHTML = '';
    if (food.tags) {
        const tags = food.tags.split(',');
        tags.slice(0, 4).forEach(tag => {
            const tagEl = document.createElement('span');
            tagEl.className = 'food-tag';
            tagEl.textContent = tag.trim();
            tagsEl.appendChild(tagEl);
        });
    }
}

// Display differences
function displayDifferences(differences) {
    const metrics = [
        { key: 'calories', label: 'Calories', unit: 'kcal' },
        { key: 'protein_g', label: 'Protein', unit: 'g' },
        { key: 'carbs_g', label: 'Carbs', unit: 'g' },
        { key: 'fat_g', label: 'Fat', unit: 'g' },
        { key: 'fiber_g', label: 'Fiber', unit: 'g' },
        { key: 'sugar_g', label: 'Sugar', unit: 'g' },
        { key: 'sodium_mg', label: 'Sodium', unit: 'mg' }
    ];
    
    metrics.forEach(metric => {
        const diffRow = document.querySelector(`.diff-row[data-metric="${metric.key.replace('_g', '').replace('_mg', '')}"]`);
        const diff = differences[metric.key];
        
        if (diff === 0) {
            diffRow.innerHTML = `<i class="fas fa-equals"></i> <span>Equal</span>`;
            diffRow.className = 'diff-row neutral';
        } else if (diff > 0) {
            diffRow.innerHTML = `<i class="fas fa-arrow-right"></i> <span>+${Math.abs(diff).toFixed(1)} ${metric.unit}</span>`;
            diffRow.className = 'diff-row positive';
        } else {
            diffRow.innerHTML = `<i class="fas fa-arrow-left"></i> <span>-${Math.abs(diff).toFixed(1)} ${metric.unit}</span>`;
            diffRow.className = 'diff-row negative';
        }
    });
}

// Display health analysis
function displayHealthAnalysis(analysis) {
    const banner = document.getElementById('healthAnalysis');
    
    if (analysis.winner === 'tie') {
        banner.className = 'health-analysis-banner tie';
        banner.innerHTML = `
            <i class="fas fa-balance-scale"></i>
            <div>
                <h3>It's a Tie!</h3>
                <p>Both foods have equal health scores</p>
            </div>
        `;
    } else {
        banner.className = 'health-analysis-banner winner';
        banner.innerHTML = `
            <i class="fas fa-trophy"></i>
            <div>
                <h3>${analysis.winner} is Healthier</h3>
                <ul>
                    ${analysis.reasons.map(reason => `<li>${reason}</li>`).join('')}
                </ul>
            </div>
        `;
    }
}

// Create macro pie charts
function createMacroCharts(food1, food2) {
    // Destroy existing charts
    if (macroChart1) macroChart1.destroy();
    if (macroChart2) macroChart2.destroy();
    
    const chartOptions = {
        type: 'doughnut',
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { font: { size: 10 } }
                }
            }
        }
    };
    
    // Chart 1
    const ctx1 = document.getElementById('macroChart1').getContext('2d');
    macroChart1 = new Chart(ctx1, {
        ...chartOptions,
        data: {
            labels: ['Protein', 'Carbs', 'Fat'],
            datasets: [{
                data: [food1.protein_g || 0, food1.carbs_g || 0, food1.fat_g || 0],
                backgroundColor: ['#ff6b6b', '#4ecdc4', '#ffe66d']
            }]
        }
    });
    
    // Chart 2
    const ctx2 = document.getElementById('macroChart2').getContext('2d');
    macroChart2 = new Chart(ctx2, {
        ...chartOptions,
        data: {
            labels: ['Protein', 'Carbs', 'Fat'],
            datasets: [{
                data: [food2.protein_g || 0, food2.carbs_g || 0, food2.fat_g || 0],
                backgroundColor: ['#ff6b6b', '#4ecdc4', '#ffe66d']
            }]
        }
    });
}

// Create comparison bar chart
function createComparisonChart(food1, food2) {
    if (comparisonChart) comparisonChart.destroy();
    
    const ctx = document.getElementById('comparisonBarChart').getContext('2d');
    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Fiber (g)', 'Sugar (g)'],
            datasets: [
                {
                    label: food1.name,
                    data: [
                        food1.calories || 0,
                        food1.protein_g || 0,
                        food1.carbs_g || 0,
                        food1.fat_g || 0,
                        food1.fiber_g || 0,
                        food1.sugar_g || 0
                    ],
                    backgroundColor: 'rgba(124, 77, 255, 0.6)',
                    borderColor: 'rgba(124, 77, 255, 1)',
                    borderWidth: 2
                },
                {
                    label: food2.name,
                    data: [
                        food2.calories || 0,
                        food2.protein_g || 0,
                        food2.carbs_g || 0,
                        food2.fat_g || 0,
                        food2.fiber_g || 0,
                        food2.sugar_g || 0
                    ],
                    backgroundColor: 'rgba(78, 205, 196, 0.6)',
                    borderColor: 'rgba(78, 205, 196, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
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

// Create difference chart
function createDifferenceChart(differences) {
    if (differenceChart) differenceChart.destroy();
    
    const ctx = document.getElementById('differenceChart').getContext('2d');
    differenceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Cal', 'Pro', 'Carb', 'Fat'],
            datasets: [{
                label: 'Difference',
                data: [
                    differences.calories || 0,
                    differences.protein_g || 0,
                    differences.carbs_g || 0,
                    differences.fat_g || 0
                ],
                backgroundColor: function(context) {
                    const value = context.raw;
                    return value > 0 ? 'rgba(78, 205, 196, 0.6)' : 'rgba(255, 107, 107, 0.6)';
                },
                borderColor: function(context) {
                    const value = context.raw;
                    return value > 0 ? 'rgba(78, 205, 196, 1)' : 'rgba(255, 107, 107, 1)';
                },
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: { display: false }
                }
            }
        }
    });
}
