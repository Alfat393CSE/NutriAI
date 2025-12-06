// Profile Management JavaScript

document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
    
    // Auto-calculate BMI when height/weight changes
    document.getElementById('height')?.addEventListener('input', calculateBMI);
    document.getElementById('weight')?.addEventListener('input', calculateBMI);
});

async function loadProfile() {
    try {
        const profile = await window.nutriAI.apiRequest('/api/profile');
        
        // Account info
        document.getElementById('username').value = profile.username || '';
        document.getElementById('email').value = profile.email || '';
        document.getElementById('fullName').value = profile.full_name || '';
        
        // Health metrics
        document.getElementById('age').value = profile.age || '';
        document.getElementById('gender').value = profile.gender || '';
        document.getElementById('height').value = profile.height || '';
        document.getElementById('weight').value = profile.weight || '';
        document.getElementById('bmi').value = profile.bmi || '';
        
        // Dietary preferences
        document.getElementById('dietGoal').value = profile.diet_goal || '';
        document.getElementById('dietaryType').value = profile.dietary_type || '';
        document.getElementById('allergies').value = profile.allergies?.join(', ') || '';
        document.getElementById('activityLevel').value = profile.activity_level || '';
        
        // Daily targets
        document.getElementById('caloriesGoal').value = profile.calories_goal || '';
        document.getElementById('proteinGoal').value = profile.protein_goal || '';
        document.getElementById('carbsGoal').value = profile.carbs_goal || '';
        document.getElementById('fatGoal').value = profile.fat_goal || '';
        
    } catch (error) {
        console.error('Failed to load profile:', error);
    }
}

function calculateBMI() {
    const height = parseFloat(document.getElementById('height')?.value);
    const weight = parseFloat(document.getElementById('weight')?.value);
    
    if (height && weight && height > 0) {
        const heightInMeters = height / 100;
        const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1);
        document.getElementById('bmi').value = bmi;
    }
}

async function saveProfile() {
    try {
        // Collect all form data
        const data = {
            full_name: document.getElementById('fullName')?.value,
            age: parseInt(document.getElementById('age')?.value) || null,
            gender: document.getElementById('gender')?.value,
            height: parseFloat(document.getElementById('height')?.value) || null,
            weight: parseFloat(document.getElementById('weight')?.value) || null,
            diet_goal: document.getElementById('dietGoal')?.value,
            dietary_type: document.getElementById('dietaryType')?.value,
            allergies: document.getElementById('allergies')?.value
                .split(',')
                .map(a => a.trim())
                .filter(a => a),
            activity_level: document.getElementById('activityLevel')?.value,
            calories_goal: parseInt(document.getElementById('caloriesGoal')?.value) || null,
            protein_goal: parseInt(document.getElementById('proteinGoal')?.value) || null,
            carbs_goal: parseInt(document.getElementById('carbsGoal')?.value) || null,
            fat_goal: parseInt(document.getElementById('fatGoal')?.value) || null
        };
        
        await window.nutriAI.apiRequest('/api/profile', 'PUT', data);
        window.nutriAI.showToast('Profile updated successfully!', 'success');
        
        // Reload to show updated BMI
        await loadProfile();
        
    } catch (error) {
        console.error('Failed to save profile:', error);
    }
}

// Add profile-specific CSS
const profileStyles = document.createElement('style');
profileStyles.textContent = `
    .profile-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 24px;
        margin-bottom: 24px;
    }
    
    .form-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
    }
    
    .form-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .form-group.full-width {
        grid-column: 1 / -1;
    }
    
    .form-group label {
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    .form-group input,
    .form-group select {
        padding: 10px 12px;
        border: 1px solid var(--gray-300);
        border-radius: var(--border-radius);
        font-size: 0.95rem;
        transition: var(--transition);
    }
    
    .form-group input:focus,
    .form-group select:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .form-group input:disabled {
        background: var(--bg-secondary);
        cursor: not-allowed;
    }
    
    .profile-actions {
        display: flex;
        gap: 12px;
        justify-content: center;
        padding: 24px;
        background: white;
        border-radius: var(--border-radius-lg);
    }
    
    @media (max-width: 768px) {
        .profile-grid {
            grid-template-columns: 1fr;
        }
        .form-grid {
            grid-template-columns: 1fr;
        }
    }
`;
document.head.appendChild(profileStyles);
