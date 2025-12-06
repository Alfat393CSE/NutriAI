// Admin Panel JavaScript

// Utility Functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        showToast(error.message, 'error');
        throw error;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadAdminStats();
    await loadUsers();
});

async function loadAdminStats() {
    try {
        const stats = await apiRequest('/api/admin/stats');
        
        document.getElementById('totalUsers').textContent = stats.users.total;
        document.getElementById('totalFoods').textContent = stats.content.total_foods;
        document.getElementById('totalPlans').textContent = stats.content.total_meal_plans;
        document.getElementById('totalLogs').textContent = stats.content.total_food_logs;
        document.getElementById('newUsers').textContent = stats.users.new_this_week || 0;
    } catch (error) {
        console.error('Failed to load admin stats:', error);
    }
}

async function loadUsers() {
    try {
        const users = await apiRequest('/api/admin/users');
        displayUsersTable(users);
    } catch (error) {
        document.getElementById('usersTable').innerHTML = '<p>Failed to load users</p>';
    }
}

function displayUsersTable(users) {
    const table = `
        <table class="admin-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Admin</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${users.map(user => `
                    <tr>
                        <td>#${user.id}</td>
                        <td><strong>${user.username}</strong></td>
                        <td>${user.email}</td>
                        <td>
                            <span class="admin-badge ${user.is_admin ? 'success' : 'info'}">
                                ${user.is_admin ? '<i class="fas fa-shield-alt"></i> Admin' : '<i class="fas fa-user"></i> User'}
                            </span>
                        </td>
                        <td>
                            <span class="admin-badge ${user.is_active ? 'success' : 'danger'}">
                                ${user.is_active ? '<i class="fas fa-check-circle"></i> Active' : '<i class="fas fa-times-circle"></i> Inactive'}
                            </span>
                        </td>
                        <td>${new Date(user.created_at).toLocaleDateString()}</td>
                        <td>
                            <button class="admin-btn admin-btn-sm ${user.is_active ? 'admin-btn-danger' : 'admin-btn-success'}" onclick="toggleUserStatus(${user.id})" title="${user.is_active ? 'Deactivate' : 'Activate'}">
                                <i class="fas fa-${user.is_active ? 'ban' : 'check'}"></i>
                            </button>
                            ${!user.is_admin ? `
                                <button class="admin-btn admin-btn-primary admin-btn-sm" onclick="makeAdmin(${user.id})" title="Make Admin">
                                    <i class="fas fa-shield-alt"></i>
                                </button>
                            ` : ''}
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    document.getElementById('usersTable').innerHTML = table;
}

async function toggleUserStatus(userId) {
    try {
        await apiRequest(`/api/admin/users/${userId}/toggle-active`, 'POST');
        showToast('User status updated', 'success');
        await loadUsers();
    } catch (error) {
        // Error handled
    }
}

async function makeAdmin(userId) {
    if (!confirm('Grant admin privileges to this user?')) return;
    
    try {
        await apiRequest(`/api/admin/users/${userId}/make-admin`, 'POST');
        showToast('Admin privileges granted', 'success');
        await loadUsers();
    } catch (error) {
        // Error handled
    }
}

function refreshUsers() {
    loadUsers();
}

function showTab(tabName) {
    // Update tab buttons (if they exist)
    const tabButtons = document.querySelectorAll('.admin-tab-btn');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    const activeTabBtn = Array.from(tabButtons).find(btn => 
        btn.textContent.toLowerCase().includes(tabName.toLowerCase())
    );
    if (activeTabBtn) {
        activeTabBtn.classList.add('active');
    }
    
    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
    const targetPane = document.getElementById(tabName + 'Tab');
    if (targetPane) {
        targetPane.classList.add('active');
    }
    
    // Load content for tab
    if (tabName === 'foods') {
        loadFoodsAdmin();
    } else if (tabName === 'analytics') {
        loadAnalytics();
    } else if (tabName === 'logs') {
        loadAdminLogs();
    }
}

async function loadFoodsAdmin() {
    try {
        const foods = await apiRequest('/api/admin/foods');
        
        const table = `
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Health Score</th>
                        <th>Calories</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${foods.map(food => `
                        <tr>
                            <td>#${food.id}</td>
                            <td><strong>${food.name}</strong></td>
                            <td><span class="admin-badge info">${food.category || 'N/A'}</span></td>
                            <td><span class="admin-badge ${food.health_score > 70 ? 'success' : food.health_score > 50 ? 'warning' : 'danger'}">${food.health_score || 'N/A'}</span></td>
                            <td>${food.calories || 0} cal</td>
                            <td>
                                <button class="admin-btn admin-btn-danger admin-btn-sm" onclick="deleteFood(${food.id})" title="Delete Food">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        document.getElementById('foodsTable').innerHTML = table;
    } catch (error) {
        document.getElementById('foodsTable').innerHTML = '<p>Failed to load foods</p>';
    }
}

async function deleteFood(foodId) {
    if (!confirm('Delete this food? This action cannot be undone.')) return;
    
    try {
        await apiRequest(`/api/admin/foods/${foodId}`, 'DELETE');
        showToast('Food deleted', 'success');
        await loadFoodsAdmin();
    } catch (error) {
        // Error handled
    }
}

async function loadAnalytics() {
    try {
        const dietGoals = await apiRequest('/api/admin/analytics/diet-goals');
        
        const ctx = document.getElementById('analyticsChart');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(dietGoals),
                datasets: [{
                    label: 'Users by Diet Goal',
                    data: Object.values(dietGoals),
                    backgroundColor: [
                        '#6366f1',
                        '#22c55e',
                        '#f97316',
                        '#ec4899',
                        '#3b82f6'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    } catch (error) {
        console.error('Failed to load analytics:', error);
    }
}

async function loadAdminLogs() {
    try {
        const logs = await apiRequest('/api/admin/logs');
        
        const table = `
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Admin</th>
                        <th>Action</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    ${logs.map(log => `
                        <tr>
                            <td>${new Date(log.timestamp).toLocaleString()}</td>
                            <td><strong>${log.admin}</strong></td>
                            <td><span class="admin-badge info"><i class="fas fa-bolt"></i> ${log.action}</span></td>
                            <td>${log.details}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        document.getElementById('logsTable').innerHTML = table;
    } catch (error) {
        document.getElementById('logsTable').innerHTML = '<p>Failed to load logs</p>';
    }
}

function showAddFoodModal() {
    showToast('Add food feature coming soon!', 'info');
}

// Initialize admin dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    // Load initial stats
    loadAdminStats();
    
    // Load users by default
    loadUsers();
});
