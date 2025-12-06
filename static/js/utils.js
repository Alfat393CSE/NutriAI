// Utility Functions for NutriAI

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

// Keyboard shortcut handler
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K: Quick search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        openQuickSearch();
    }
    
    // Ctrl/Cmd + B: Go to dashboard
    if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
        e.preventDefault();
        window.location.href = '/dashboard';
    }
    
    // Ctrl/Cmd + Shift + A: Quick add food
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'A') {
        e.preventDefault();
        quickAddFood();
    }
    
    // Ctrl/Cmd + Shift + D: Toggle dark mode
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
        e.preventDefault();
        if (typeof toggleTheme === 'function') {
            toggleTheme();
        }
    }
    
    // Escape: Close any open modal
    if (e.key === 'Escape') {
        closeAllModals();
    }
});

// ============================================
// QUICK ACTIONS
// ============================================

// Quick search modal
function openQuickSearch() {
    let quickSearchModal = document.getElementById('quickSearchModal');
    
    if (!quickSearchModal) {
        // Create quick search modal
        quickSearchModal = document.createElement('div');
        quickSearchModal.id = 'quickSearchModal';
        quickSearchModal.className = 'modal active';
        quickSearchModal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3><i class="fas fa-search"></i> Quick Search</h3>
                    <button class="modal-close" onclick="closeQuickSearch()" aria-label="Close modal">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <input type="text" id="quickSearchInput" class="form-control" 
                           placeholder="Search foods, navigate pages..." autofocus>
                    <div id="quickSearchResults" class="quick-search-results"></div>
                </div>
            </div>
        `;
        document.body.appendChild(quickSearchModal);
        
        // Add event listener for search
        const searchInput = document.getElementById('quickSearchInput');
        searchInput.addEventListener('input', handleQuickSearch);
        searchInput.focus();
    } else {
        quickSearchModal.classList.add('active');
        document.getElementById('quickSearchInput').focus();
    }
}

function closeQuickSearch() {
    const modal = document.getElementById('quickSearchModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Handle quick search
async function handleQuickSearch(e) {
    const query = e.target.value.toLowerCase();
    const resultsContainer = document.getElementById('quickSearchResults');
    
    if (query.length < 2) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    // Navigation shortcuts
    const pages = [
        { name: 'Dashboard', url: '/dashboard', icon: 'fa-home', keywords: ['home', 'dashboard', 'main'] },
        { name: 'Food Search', url: '/food-search', icon: 'fa-search', keywords: ['food', 'search', 'browse'] },
        { name: 'Meal Planner', url: '/meal-planner', icon: 'fa-calendar-alt', keywords: ['meal', 'plan', 'schedule'] },
        { name: 'AI Assistant', url: '/chatbot', icon: 'fa-comments', keywords: ['chat', 'bot', 'assistant', 'ai'] },
        { name: 'Profile', url: '/profile', icon: 'fa-user', keywords: ['profile', 'settings', 'account'] },
        { name: 'History', url: '/history', icon: 'fa-history', keywords: ['history', 'past', 'records'] },
        { name: 'Food Comparison', url: '/food-comparison', icon: 'fa-balance-scale', keywords: ['compare', 'comparison', 'vs'] }
    ];
    
    const matchedPages = pages.filter(page => 
        page.name.toLowerCase().includes(query) || 
        page.keywords.some(kw => kw.includes(query))
    );
    
    let resultsHTML = '';
    
    // Show matched pages
    if (matchedPages.length > 0) {
        resultsHTML += '<div class="search-category">Pages</div>';
        matchedPages.forEach(page => {
            resultsHTML += `
                <div class="search-result-item" onclick="window.location.href='${page.url}'">
                    <i class="fas ${page.icon}"></i>
                    <span>${page.name}</span>
                </div>
            `;
        });
    }
    
    // Search foods if API is available
    try {
        if (window.nutriAI) {
            const foods = await window.nutriAI.apiRequest(`/api/foods?search=${query}&limit=5`);
            if (foods && foods.length > 0) {
                resultsHTML += '<div class="search-category">Foods</div>';
                foods.forEach(food => {
                    resultsHTML += `
                        <div class="search-result-item" onclick="viewFood(${food.id})">
                            <i class="fas fa-apple-alt"></i>
                            <span>${food.name}</span>
                            <small>${food.calories} cal</small>
                        </div>
                    `;
                });
            }
        }
    } catch (error) {
        console.error('Error searching foods:', error);
    }
    
    if (resultsHTML === '') {
        resultsHTML = '<div class="no-results">No results found</div>';
    }
    
    resultsContainer.innerHTML = resultsHTML;
}

// Quick add food
function quickAddFood() {
    // If on dashboard, trigger the log food modal
    if (window.location.pathname === '/dashboard') {
        const logFoodBtn = document.querySelector('[onclick="openModal(\'logFoodModal\')"]');
        if (logFoodBtn) {
            logFoodBtn.click();
            return;
        }
    }
    
    // Otherwise, navigate to food search
    window.location.href = '/food-search';
}

// View food details
function viewFood(foodId) {
    closeQuickSearch();
    window.location.href = `/food-search?food=${foodId}`;
}

// Close all modals
function closeAllModals() {
    document.querySelectorAll('.modal.active').forEach(modal => {
        modal.classList.remove('active');
    });
}

// ============================================
// DATA EXPORT
// ============================================

// Export data as CSV
function exportToCSV(data, filename) {
    if (!data || data.length === 0) {
        showToast('No data to export', 'error');
        return;
    }
    
    // Get headers from first object
    const headers = Object.keys(data[0]);
    
    // Create CSV content
    let csv = headers.join(',') + '\n';
    
    data.forEach(row => {
        const values = headers.map(header => {
            let value = row[header];
            // Handle values with commas or quotes
            if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                value = `"${value.replace(/"/g, '""')}"`;
            }
            return value;
        });
        csv += values.join(',') + '\n';
    });
    
    // Create download link
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `${filename}_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast('Data exported successfully!', 'success');
}

// Export nutrition data
async function exportNutritionData() {
    try {
        // Get user's food logs
        const logs = await window.nutriAI.apiRequest('/api/food-logs?limit=1000');
        
        if (!logs || logs.length === 0) {
            showToast('No nutrition data to export', 'info');
            return;
        }
        
        // Format data for export
        const exportData = logs.map(log => ({
            Date: log.date,
            'Food Name': log.food_name,
            'Meal Type': log.meal_type,
            Calories: log.calories_consumed,
            'Protein (g)': log.protein_consumed,
            'Carbs (g)': log.carbs_consumed,
            'Fat (g)': log.fat_consumed
        }));
        
        exportToCSV(exportData, 'nutriai_nutrition_data');
    } catch (error) {
        console.error('Error exporting data:', error);
        showToast('Failed to export data', 'error');
    }
}

// Export meal plan
async function exportMealPlan() {
    try {
        // Get active meal plan
        const stats = await window.nutriAI.apiRequest('/api/dashboard/stats');
        
        if (!stats.active_meal_plan) {
            showToast('No active meal plan to export', 'info');
            return;
        }
        
        const plan = stats.active_meal_plan;
        
        // Format meal plan data
        const exportData = [];
        
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].forEach(day => {
            const dayKey = day.toLowerCase();
            const dayPlan = plan[dayKey];
            
            if (dayPlan) {
                ['Breakfast', 'Lunch', 'Dinner'].forEach(meal => {
                    const mealKey = meal.toLowerCase();
                    if (dayPlan[mealKey]) {
                        exportData.push({
                            Day: day,
                            Meal: meal,
                            'Food Name': dayPlan[mealKey].name,
                            Calories: dayPlan[mealKey].calories,
                            'Protein (g)': dayPlan[mealKey].protein_g,
                            'Carbs (g)': dayPlan[mealKey].carbs_g,
                            'Fat (g)': dayPlan[mealKey].fat_g
                        });
                    }
                });
            }
        });
        
        exportToCSV(exportData, `nutriai_meal_plan_${plan.name.replace(/\s+/g, '_')}`);
    } catch (error) {
        console.error('Error exporting meal plan:', error);
        showToast('Failed to export meal plan', 'error');
    }
}

// Export history
async function exportHistory() {
    try {
        const history = await window.nutriAI.apiRequest('/api/history?days=90');
        
        if (!history || history.length === 0) {
            showToast('No history data to export', 'info');
            return;
        }
        
        const exportData = history.map(item => ({
            Date: new Date(item.timestamp).toLocaleDateString(),
            Time: new Date(item.timestamp).toLocaleTimeString(),
            Action: item.action_type,
            'Food Name': item.food_name || 'N/A',
            Calories: item.calories || 'N/A',
            'Search Query': item.search_query || 'N/A'
        }));
        
        exportToCSV(exportData, 'nutriai_history');
    } catch (error) {
        console.error('Error exporting history:', error);
        showToast('Failed to export history', 'error');
    }
}

// ============================================
// LOADING STATES
// ============================================

// Show loading overlay
function showLoading(message = 'Loading...') {
    let overlay = document.getElementById('loadingOverlay');
    
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>${message}</p>
            </div>
        `;
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        `;
        document.body.appendChild(overlay);
    } else {
        overlay.style.display = 'flex';
        overlay.querySelector('p').textContent = message;
    }
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// ============================================
// HELPER FUNCTIONS
// ============================================

// Format date
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show keyboard shortcuts help
function showKeyboardShortcuts() {
    const shortcuts = [
        { keys: 'Ctrl/Cmd + K', action: 'Quick Search' },
        { keys: 'Ctrl/Cmd + B', action: 'Go to Dashboard' },
        { keys: 'Ctrl/Cmd + Shift + A', action: 'Quick Add Food' },
        { keys: 'Ctrl/Cmd + Shift + D', action: 'Toggle Dark Mode' },
        { keys: 'Esc', action: 'Close Modal' }
    ];
    
    let html = '<div class="shortcuts-help"><h3>Keyboard Shortcuts</h3><ul>';
    shortcuts.forEach(s => {
        html += `<li><kbd>${s.keys}</kbd> <span>${s.action}</span></li>`;
    });
    html += '</ul></div>';
    
    showToast(html, 'info');
}

// Initialize utility features
document.addEventListener('DOMContentLoaded', () => {
    console.log('NutriAI Utils loaded - Keyboard shortcuts active!');
});
