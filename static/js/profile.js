// Profile Management JavaScript

document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
    loadProfileStats();
    
    // Auto-calculate BMI when height/weight changes
    document.getElementById('height')?.addEventListener('input', calculateBMI);
    document.getElementById('weight')?.addEventListener('input', calculateBMI);
    
    // Add input animations
    addInputAnimations();
});

async function loadProfile() {
    try {
        const profile = await window.nutriAI.apiRequest('/api/profile');
        
        // Update profile header
        const displayName = document.getElementById('profileDisplayName');
        const emailDisplay = document.getElementById('profileEmail');
        if (displayName) displayName.textContent = profile.full_name || profile.username || 'User';
        if (emailDisplay) emailDisplay.textContent = profile.email || '';
        
        // Account info
        const username = document.getElementById('username');
        const email = document.getElementById('email');
        const fullName = document.getElementById('fullName');
        if (username) username.value = profile.username || '';
        if (email) email.value = profile.email || '';
        if (fullName) fullName.value = profile.full_name || '';
        
        // Health metrics - map backend field names to frontend
        const age = document.getElementById('age');
        const gender = document.getElementById('gender');
        const height = document.getElementById('height');
        const weight = document.getElementById('weight');
        const bmi = document.getElementById('bmi');
        if (age) age.value = profile.age || '';
        if (gender) gender.value = profile.gender || '';
        if (height) height.value = profile.height_cm || '';
        if (weight) weight.value = profile.weight_kg || '';
        if (bmi) bmi.value = profile.bmi || '';
        
        // Calculate and display BMI status
        if (profile.bmi) {
            updateBMIStatus(profile.bmi);
        }
        
        // Dietary preferences - map backend field names to frontend
        const dietGoal = document.getElementById('dietGoal');
        const dietaryType = document.getElementById('dietaryType');
        const allergies = document.getElementById('allergies');
        const activityLevel = document.getElementById('activityLevel');
        if (dietGoal) dietGoal.value = profile.diet_goal || '';
        if (dietaryType) dietaryType.value = profile.dietary_restrictions || '';
        if (allergies) allergies.value = Array.isArray(profile.allergies) ? profile.allergies.join(', ') : (profile.allergies || '');
        if (activityLevel) activityLevel.value = profile.physical_activity_level || '';
        
        // Daily targets - map backend field names to frontend
        const caloriesGoal = document.getElementById('caloriesGoal');
        const proteinGoal = document.getElementById('proteinGoal');
        const carbsGoal = document.getElementById('carbsGoal');
        const fatGoal = document.getElementById('fatGoal');
        if (caloriesGoal) caloriesGoal.value = profile.daily_caloric_intake || '';
        if (proteinGoal) proteinGoal.value = profile.protein_goal || '';
        if (carbsGoal) carbsGoal.value = profile.carbs_goal || '';
        if (fatGoal) fatGoal.value = profile.fat_goal || '';
        
    } catch (error) {
        console.error('Failed to load profile:', error);
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Failed to load profile data', 'error');
        }
    }
}

async function loadProfileStats() {
    try {
        // Mock data for demo - replace with actual API calls
        const streakDays = document.getElementById('streakDays');
        const mealsLogged = document.getElementById('mealsLogged');
        const goalsAchieved = document.getElementById('goalsAchieved');
        
        if (streakDays) streakDays.textContent = '7';
        if (mealsLogged) mealsLogged.textContent = '42';
        if (goalsAchieved) goalsAchieved.textContent = '15';
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Reset profile to last saved values
async function resetProfile() {
    try {
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Resetting to last saved values...', 'info');
        }
        await loadProfile();
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Profile reset successfully!', 'success');
        }
    } catch (error) {
        console.error('Failed to reset profile:', error);
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Failed to reset profile', 'error');
        }
    }
}

function calculateBMI() {
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const bmiInput = document.getElementById('bmi');
    
    if (!heightInput || !weightInput || !bmiInput) return;
    
    const height = parseFloat(heightInput.value);
    const weight = parseFloat(weightInput.value);
    
    if (height && weight && height > 0) {
        const heightInMeters = height / 100;
        const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1);
        bmiInput.value = bmi;
        updateBMIStatus(bmi);
    }
}

function updateBMIStatus(bmi) {
    const bmiStatusElement = document.getElementById('bmiStatus');
    if (!bmiStatusElement) return;
    
    let status = '';
    let className = '';
    
    if (bmi < 18.5) {
        status = 'Underweight';
        className = 'status-warning';
    } else if (bmi >= 18.5 && bmi < 25) {
        status = 'Healthy';
        className = 'status-success';
    } else if (bmi >= 25 && bmi < 30) {
        status = 'Overweight';
        className = 'status-warning';
    } else {
        status = 'Obese';
        className = 'status-danger';
    }
    
    bmiStatusElement.textContent = status;
    bmiStatusElement.className = `bmi-status ${className}`;
}

function calculateTargets() {
    const ageInput = document.getElementById('age');
    const genderInput = document.getElementById('gender');
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const activityLevelInput = document.getElementById('activityLevel');
    const dietGoalInput = document.getElementById('dietGoal');
    
    if (!ageInput || !genderInput || !heightInput || !weightInput || !activityLevelInput) {
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Please fill in all health metrics first', 'warning');
        }
        return;
    }
    
    const age = parseInt(ageInput.value);
    const gender = genderInput.value;
    const height = parseFloat(heightInput.value);
    const weight = parseFloat(weightInput.value);
    const activityLevel = activityLevelInput.value;
    const dietGoal = dietGoalInput ? dietGoalInput.value : '';
    
    if (!age || !gender || !height || !weight || !activityLevel) {
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Please fill in all health metrics first', 'warning');
        }
        return;
    }
    
    // Calculate BMR using Mifflin-St Jeor Equation
    let bmr;
    if (gender === 'male') {
        bmr = 10 * weight + 6.25 * height - 5 * age + 5;
    } else {
        bmr = 10 * weight + 6.25 * height - 5 * age - 161;
    }
    
    // Activity multipliers
    const activityMultipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    };
    
    let tdee = bmr * (activityMultipliers[activityLevel] || 1.2);
    
    // Adjust based on diet goal
    if (dietGoal === 'weight_loss') {
        tdee *= 0.85; // 15% deficit
    } else if (dietGoal === 'muscle_gain') {
        tdee *= 1.1; // 10% surplus
    }
    
    // Calculate macros
    const protein = Math.round(weight * 2); // 2g per kg
    const fat = Math.round(tdee * 0.25 / 9); // 25% of calories
    const carbs = Math.round((tdee - (protein * 4) - (fat * 9)) / 4);
    
    // Update fields
    const caloriesGoalInput = document.getElementById('caloriesGoal');
    const proteinGoalInput = document.getElementById('proteinGoal');
    const carbsGoalInput = document.getElementById('carbsGoal');
    const fatGoalInput = document.getElementById('fatGoal');
    
    if (caloriesGoalInput) caloriesGoalInput.value = Math.round(tdee);
    if (proteinGoalInput) proteinGoalInput.value = protein;
    if (carbsGoalInput) carbsGoalInput.value = carbs;
    if (fatGoalInput) fatGoalInput.value = fat;
    
    if (window.nutriAI && window.nutriAI.showToast) {
        window.nutriAI.showToast('Nutritional targets calculated based on your profile!', 'success');
    }
}

async function saveProfile(event) {
    // Get button reference before async operations
    const saveBtn = event?.currentTarget || document.querySelector('.btn-primary.btn-lg');
    
    try {
        // Show loading state
        if (saveBtn) {
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
        }
        
        // Get allergies value safely
        const allergiesInput = document.getElementById('allergies');
        const allergiesValue = allergiesInput?.value || '';
        
        // Collect all form data with correct field names matching backend
        const data = {
            age: parseInt(document.getElementById('age')?.value) || null,
            gender: document.getElementById('gender')?.value || null,
            height_cm: parseFloat(document.getElementById('height')?.value) || null,
            weight_kg: parseFloat(document.getElementById('weight')?.value) || null,
            diet_goal: document.getElementById('dietGoal')?.value || null,
            dietary_restrictions: document.getElementById('dietaryType')?.value || null,
            allergies: allergiesValue
                .split(',')
                .map(a => a.trim())
                .filter(a => a),
            physical_activity_level: document.getElementById('activityLevel')?.value || null,
            daily_caloric_intake: parseInt(document.getElementById('caloriesGoal')?.value) || null,
            protein_goal: parseInt(document.getElementById('proteinGoal')?.value) || null,
            carbs_goal: parseInt(document.getElementById('carbsGoal')?.value) || null,
            fat_goal: parseInt(document.getElementById('fatGoal')?.value) || null,
            full_name: document.getElementById('fullName')?.value || null
        };
        
        // Remove null values
        Object.keys(data).forEach(key => {
            if (data[key] === null || data[key] === '') {
                delete data[key];
            }
        });
        
        if (window.nutriAI && window.nutriAI.apiRequest) {
            const response = await window.nutriAI.apiRequest('/api/profile', 'PUT', data);
            
            if (window.nutriAI.showToast) {
                window.nutriAI.showToast('Profile updated successfully! 🎉', 'success');
            }
            
            // Reload profile data to ensure UI is in sync with backend
            await loadProfile();
        }
        
    } catch (error) {
        console.error('Failed to save profile:', error);
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Failed to save profile. Please try again.', 'error');
        }
    } finally {
        // Reset button state
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save"></i> Save All Changes';
        }
    }
}

function exportProfile() {
    try {
        const profile = {
            username: document.getElementById('username')?.value,
            email: document.getElementById('email')?.value,
            fullName: document.getElementById('fullName')?.value,
            age: document.getElementById('age')?.value,
            gender: document.getElementById('gender')?.value,
            height: document.getElementById('height')?.value,
            weight: document.getElementById('weight')?.value,
            bmi: document.getElementById('bmi')?.value,
            dietGoal: document.getElementById('dietGoal')?.value,
            dietaryType: document.getElementById('dietaryType')?.value,
            allergies: document.getElementById('allergies')?.value,
            activityLevel: document.getElementById('activityLevel')?.value,
            caloriesGoal: document.getElementById('caloriesGoal')?.value,
            proteinGoal: document.getElementById('proteinGoal')?.value,
            carbsGoal: document.getElementById('carbsGoal')?.value,
            fatGoal: document.getElementById('fatGoal')?.value
        };
        
        const dataStr = JSON.stringify(profile, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `nutriai-profile-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        URL.revokeObjectURL(url);
        
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Profile exported successfully!', 'success');
        }
    } catch (error) {
        console.error('Failed to export profile:', error);
        if (window.nutriAI && window.nutriAI.showToast) {
            window.nutriAI.showToast('Failed to export profile', 'error');
        }
    }
}

function addInputAnimations() {
    const inputs = document.querySelectorAll('input:not([disabled]), select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Add change detection for visual feedback
        input.addEventListener('input', function() {
            if (this.value) {
                this.style.borderColor = '#10b981';
                setTimeout(() => {
                    this.style.borderColor = '';
                }, 300);
            }
        });
    });
    
    // Add stagger animation to cards on page load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });
    
    // Animate profile header
    const profileHeader = document.querySelector('.profile-header');
    if (profileHeader) {
        profileHeader.style.opacity = '0';
        profileHeader.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            profileHeader.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            profileHeader.style.opacity = '1';
            profileHeader.style.transform = 'translateY(0)';
        }, 50);
    }
}

// Custom toast notification
function showCustomToast(message, type = 'success') {
    const toast = document.getElementById('profileToast');
    const toastMessage = document.getElementById('toastMessage');
    
    if (toast && toastMessage) {
        toastMessage.textContent = message;
        toast.classList.add('show');
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Add profile-specific CSS
const profileStyles = document.createElement('style');
profileStyles.textContent = `
    /* Professional Profile Page Styling */
    .main-content {
        padding: 24px;
        max-width: calc(100vw - 280px - 48px); /* Account for sidebar width and padding */
        width: 100%;
        box-sizing: border-box;
    }
    
    /* Profile Header Styling */
    .profile-header {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 50%, #8b5cf6 100%);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 32px;
        color: white;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 32px;
        flex-wrap: wrap;
        position: relative;
        overflow: hidden;
        width: 100%;
        box-sizing: border-box;
    }
    
    .profile-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    
    .profile-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -5%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    
    .profile-avatar-section {
        display: flex;
        align-items: center;
        gap: 24px;
        position: relative;
        z-index: 1;
    }
    
    .profile-avatar {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
        backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
        border: 3px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3);
        position: relative;
        transition: transform 0.3s ease;
    }
    
    .profile-avatar:hover {
        transform: scale(1.05);
    }
    
    .profile-avatar::after {
        content: '';
        position: absolute;
        bottom: 5px;
        right: 5px;
        width: 24px;
        height: 24px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .profile-header-info h1 {
        font-size: 36px;
        font-weight: 800;
        margin: 0 0 8px 0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        letter-spacing: -0.5px;
    }
    
    .profile-header-info p {
        margin: 0 0 16px 0;
        opacity: 0.95;
        font-size: 15px;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    
    .profile-badges {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 13px;
        font-weight: 700;
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .badge-premium {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #78350f;
        border-color: #fcd34d;
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
    }
    
    .badge-verified {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-color: #34d399;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    
    .profile-quick-stats {
        display: flex;
        gap: 20px;
        position: relative;
        z-index: 1;
    }
    
    .quick-stat {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 20px 28px;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .quick-stat:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
    }
    
    .quick-stat i {
        font-size: 32px;
        opacity: 0.95;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    }
    
    .quick-stat strong {
        display: block;
        font-size: 28px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 4px;
    }
    
    .quick-stat span {
        display: block;
        font-size: 11px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
    }
    
    /* Profile Grid */
    .profile-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
        gap: 28px;
        margin-bottom: 28px;
        width: 100%;
        box-sizing: border-box;
    }
    
    /* Enhanced Card Styles */
    .card {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.03);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        box-sizing: border-box;
    }
    
    .card-elevated {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .card-elevated::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .card-elevated:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(99, 102, 241, 0.1);
    }
    
    .card-elevated:hover::before {
        opacity: 1;
    }
    
    .card-highlight {
        border: 2px solid transparent;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899) border-box;
        position: relative;
        overflow: visible;
    }
    
    .card-highlight::after {
        content: '⭐ RECOMMENDED';
        position: absolute;
        top: -12px;
        right: 24px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 24px 28px 20px;
        border-bottom: 2px solid rgba(0, 0, 0, 0.04);
        background: linear-gradient(to bottom, rgba(99, 102, 241, 0.02), transparent);
    }
    
    .card-header h3 {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 18px;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
        letter-spacing: -0.3px;
    }
    
    .card-header h3 i {
        color: #6366f1;
        font-size: 20px;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(99, 102, 241, 0.1);
        border-radius: 8px;
        padding: 4px;
    }
    
    .card-body {
        padding: 28px;
    }
    
    .btn-link {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.2);
        color: #6366f1;
        cursor: pointer;
        font-size: 13px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.3s ease;
        padding: 8px 16px;
        border-radius: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .btn-link:hover {
        background: #6366f1;
        color: white;
        border-color: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .btn-link i {
        font-size: 14px;
    }
    
    /* Form Styling */
    .form-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 24px;
    }
    
    .form-group {
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: relative;
    }
    
    .form-group.full-width {
        grid-column: 1 / -1;
    }
    
    .form-group.focused label {
        color: #6366f1;
    }
    
    .form-group.focused label i {
        transform: scale(1.1);
    }
    
    .form-group label {
        font-weight: 700;
        font-size: 13px;
        color: #374151;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .form-group label i {
        color: #6366f1;
        width: 18px;
        font-size: 14px;
        transition: transform 0.3s ease;
    }
    
    .form-group input,
    .form-group select {
        padding: 14px 16px;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        font-size: 15px;
        transition: all 0.3s ease;
        background: #fafafa;
        font-family: inherit;
        color: #1f2937;
        font-weight: 500;
    }
    
    .form-group input:hover:not(:disabled),
    .form-group select:hover {
        border-color: #d1d5db;
        background: white;
    }
    
    .form-group input:focus,
    .form-group select:focus {
        outline: none;
        border-color: #6366f1;
        background: white;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1), 0 1px 3px rgba(0, 0, 0, 0.05);
        transform: translateY(-1px);
    }
    
    .form-group input:disabled {
        background: #f3f4f6;
        cursor: not-allowed;
        opacity: 0.7;
        color: #6b7280;
    }
    
    .form-hint {
        font-size: 12px;
        color: #6b7280;
        font-style: italic;
        margin-top: -4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .form-hint::before {
        content: '💡';
        font-size: 14px;
    }
    
    /* BMI Display */
    .bmi-display {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    .bmi-display input {
        flex: 1;
        font-weight: 700;
        font-size: 16px;
        color: #6366f1;
    }
    
    .bmi-status {
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 12px;
        font-weight: 800;
        white-space: nowrap;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .status-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 2px solid #10b981;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fed7aa 0%, #fbbf24 100%);
        color: #78350f;
        border: 2px solid #f59e0b;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
    }
    
    .status-danger {
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
        color: #7f1d1d;
        border: 2px solid #ef4444;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
    }
    
    /* Action Buttons */
    .profile-actions {
        display: flex;
        gap: 16px;
        justify-content: center;
        padding: 36px;
        background: linear-gradient(to bottom, white, #fafafa);
        border-radius: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.03);
        flex-wrap: wrap;
        border: 1px solid rgba(0, 0, 0, 0.05);
        width: 100%;
        box-sizing: border-box;
    }
    
    .btn-lg {
        padding: 16px 36px;
        font-size: 15px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .btn-lg::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .btn-lg:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .btn-lg:active {
        transform: scale(0.97);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
    }
    
    .btn-primary:hover {
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        transform: translateY(-2px);
    }
    
    .btn-outline {
        background: white;
        color: #6366f1;
        border: 2px solid #6366f1;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .btn-outline:hover {
        background: #6366f1;
        color: white;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
    }
    
    .btn-secondary {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        color: #374151;
        border: 2px solid #d1d5db;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .btn-secondary:hover {
        background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
        border-color: #9ca3af;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .btn-lg i {
        font-size: 16px;
        transition: transform 0.3s ease;
    }
    
    .btn-lg:hover i {
        transform: scale(1.1);
    }
    
    .btn-primary:disabled {
        background: #9ca3af;
        cursor: not-allowed;
        box-shadow: none;
        opacity: 0.6;
    }
    
    .btn-primary:disabled:hover {
        transform: none;
    }
    
    /* Responsive Design */
    @media (max-width: 1024px) {
        .main-content {
            max-width: 100%;
        }
        
        .profile-header {
            flex-direction: column;
            align-items: flex-start;
            padding: 32px 28px;
        }
        
        .profile-quick-stats {
            width: 100%;
            justify-content: space-between;
        }
        
        .quick-stat {
            flex: 1;
            padding: 16px 20px;
        }
        
        .profile-grid {
            grid-template-columns: 1fr;
        }
    }
    
    @media (max-width: 768px) {
        .main-content {
            padding: 16px;
            margin-left: 0 !important; /* Remove sidebar margin on mobile */
            max-width: 100%;
        }
        
        .profile-header {
            padding: 24px 20px;
        }
        
        .profile-avatar {
            width: 90px;
            height: 90px;
            font-size: 42px;
        }
        
        .profile-header-info h1 {
            font-size: 28px;
        }
        
        .profile-grid {
            grid-template-columns: 1fr;
            gap: 20px;
        }
        
        .form-grid {
            grid-template-columns: 1fr;
            gap: 20px;
        }
        
        .card-header {
            padding: 20px 20px 16px;
        }
        
        .card-body {
            padding: 20px;
        }
        
        .profile-actions {
            flex-direction: column;
            padding: 24px 20px;
        }
        
        .btn-lg {
            width: 100%;
            justify-content: center;
            padding: 14px 24px;
        }
    }
    
    @media (max-width: 480px) {
        .profile-grid {
            grid-template-columns: 1fr !important;
        }
        
        .profile-header-info h1 {
            font-size: 24px;
        }
        
        .profile-badges {
            flex-direction: column;
            width: 100%;
        }
        
        .badge {
            width: 100%;
            justify-content: center;
        }
        
        .quick-stat i {
            font-size: 28px;
        }
        
        .quick-stat strong {
            font-size: 24px;
        }
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Smooth Transitions */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Select Styling */
    .form-group select {
        appearance: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236366f1' d='M10.293 3.293L6 7.586 1.707 3.293A1 1 0 00.293 4.707l5 5a1 1 0 001.414 0l5-5a1 1 0 10-1.414-1.414z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 12px center;
        background-size: 16px;
        padding-right: 40px;
    }
    
    /* Scrollbar Styling */
    .card-body::-webkit-scrollbar {
        width: 8px;
    }
    
    .card-body::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    .card-body::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    .card-body::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Toast Notification */
    .profile-toast {
        position: fixed;
        bottom: 32px;
        right: 32px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.4);
        display: none;
        align-items: center;
        gap: 12px;
        font-weight: 600;
        font-size: 14px;
        z-index: 1000;
        animation: slideInUp 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .profile-toast.show {
        display: flex;
    }
    
    .profile-toast i {
        font-size: 20px;
    }
    
    @keyframes slideInUp {
        from {
            transform: translateY(100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Professional Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-weight: 700;
    }
    
    /* Focus visible for accessibility */
    *:focus-visible {
        outline: 3px solid #6366f1;
        outline-offset: 2px;
        border-radius: 8px;
    }
    
    /* Card hover state for better interaction feedback */
    .card {
        will-change: transform;
    }
    
    /* Gradient text for special elements */
    .profile-header-info h1 {
        background: linear-gradient(135deg, white, rgba(255, 255, 255, 0.9));
        -webkit-background-clip: text;
        background-clip: text;
    }
`;
document.head.appendChild(profileStyles);
