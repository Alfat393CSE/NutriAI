// Auth pages JavaScript

// Toggle password visibility
document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', () => {
        const input = button.parentElement.querySelector('input');
        const icon = button.querySelector('i');
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    });
});

// Password strength checker
const passwordInput = document.getElementById('password');
if (passwordInput) {
    passwordInput.addEventListener('input', (e) => {
        const password = e.target.value;
        const strengthFill = document.querySelector('.strength-fill');
        const strengthText = document.querySelector('.strength-text');
        
        if (!strengthFill) return;
        
        let strength = 0;
        let text = 'Weak';
        let color = '#ef4444';
        
        if (password.length >= 8) strength += 25;
        if (password.match(/[a-z]+/)) strength += 25;
        if (password.match(/[A-Z]+/)) strength += 25;
        if (password.match(/[0-9]+/)) strength += 12.5;
        if (password.match(/[$@#&!]+/)) strength += 12.5;
        
        if (strength >= 75) {
            text = 'Strong';
            color = '#22c55e';
        } else if (strength >= 50) {
            text = 'Medium';
            color = '#f97316';
        }
        
        strengthFill.style.width = strength + '%';
        strengthFill.style.background = color;
        strengthText.textContent = text;
    });
}

// Register form validation
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        
        // Validation
        if (!window.nutriAI.validateEmail(email)) {
            window.nutriAI.showToast('Please enter a valid email address', 'error');
            return;
        }
        
        if (password.length < 8) {
            window.nutriAI.showToast('Password must be at least 8 characters', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            window.nutriAI.showToast('Passwords do not match', 'error');
            return;
        }
        
        try {
            const response = await window.nutriAI.apiRequest('/register', 'POST', {
                username,
                email,
                password
            });
            
            window.nutriAI.showToast('Registration successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1500);
        } catch (error) {
            // Error already shown by apiRequest
        }
    });
}

// Login form
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        // Let the form submit naturally for Flask session handling
        // If you want AJAX, uncomment below:
        /*
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await window.nutriAI.apiRequest('/login', 'POST', {
                username,
                password
            });
            
            window.nutriAI.showToast('Login successful!', 'success');
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        } catch (error) {
            // Error already shown
        }
        */
    });
}

// Social auth buttons (placeholder)
document.querySelectorAll('.btn-social').forEach(button => {
    button.addEventListener('click', () => {
        window.nutriAI.showToast('Social login coming soon!', 'info');
    });
});
