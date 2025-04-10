// Google Login
function loginWithGoogle() {
    // Use the backend's OAuth endpoint instead of directly calling Google
    window.location.href = '/auth/google';
}

// Facebook Login
function loginWithFacebook() {
    // Use the backend's OAuth endpoint instead of directly calling Facebook
    window.location.href = '/auth/facebook';
}

// Handle login form submission
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const provider = 'local';

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password, provider })
        });

        // Check if the response is JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error(`API returned non-JSON response: ${contentType}. Endpoint might not exist.`);
        }

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            window.location.href = '/dashboard';
        } else {
            throw new Error(data.detail || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert(error.message);
    }
});

// Handle registration form submission
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const provider = document.getElementById('provider').value;

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password, provider })
        });

        // Check if the response is JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error(`API returned non-JSON response: ${contentType}. Endpoint might not exist.`);
        }

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            window.location.href = '/login.html';
        } else {
            throw new Error(data.detail || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert(error.message);
    }
});
