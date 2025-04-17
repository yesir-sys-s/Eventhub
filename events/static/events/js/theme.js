document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    const icon = themeToggle.querySelector('i');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

    // Function to set theme
    function setTheme(theme) {
        if (!theme) theme = 'light'; // Fallback to light theme
        html.setAttribute('data-theme', theme);
        icon.className = `bi bi-${theme === 'light' ? 'moon-stars' : 'sun'} fs-5`;
        localStorage.setItem('theme', theme);

        // Add or remove glow effects for category navigation
        const categoryLinks = document.querySelectorAll('.category-nav a');
        categoryLinks.forEach(link => {
            if (theme === 'dark') {
                link.style.color = '#e2e2e2';
                link.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
                link.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.2)';
                link.style.border = '1px solid rgba(0, 0, 0, 0.2)';
                link.style.background = 'rgba(20, 20, 20, 0.5)';
                
                // Add stronger glow for active links
                if (link.classList.contains('fw-bold')) {
                    link.style.color = '#ffffff';
                    link.style.boxShadow = '0 0 20px rgba(0, 0, 0, 0.4)';
                    link.style.background = 'rgba(40, 40, 40, 0.8)';
                    link.style.textShadow = '0 0 10px rgba(0, 0, 0, 0.3)';
                }
            } else {
                link.style.color = '';
                link.style.boxShadow = '';
                link.style.border = '';
                link.style.background = '';
                link.style.textShadow = '';
            }
        });
    }

    // Initialize theme
    const savedTheme = localStorage.getItem('theme');
    const initialTheme = savedTheme || (prefersDark.matches ? 'dark' : 'light');
    setTheme(initialTheme);

    // Theme toggle click handler
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    });

    // Listen for system theme changes
    prefersDark.addListener((e) => {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
});
