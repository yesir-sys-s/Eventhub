'use strict';
{
    function scrollToResult(element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }

    function initSearchAnimation() {
        const searchInputs = document.querySelectorAll('.search-input');
        
        searchInputs.forEach(input => {
            // Add animated placeholder
            input.addEventListener('focus', () => {
                input.classList.add('searching');
            });
            
            // Add real-time search feedback
            input.addEventListener('input', () => {
                const val = input.value.trim();
                if (val.length > 0) {
                    input.classList.add('has-text');
                    // Find first matching result and scroll to it
                    const firstResult = document.querySelector('.search-result');
                    if (firstResult) {
                        scrollToResult(firstResult);
                    }
                } else {
                    input.classList.remove('has-text'); 
                    // Scroll back to search input
                    scrollToResult(input);
                }
            });
            
            input.addEventListener('blur', () => {
                input.classList.remove('searching');
                // Add debounced scroll restoration
                let scrollTimeout;
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(() => {
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                }, 150);
            });
        });
    }

    // Initialize when DOM is ready
    if (document.readyState !== 'loading') {
        initSearchAnimation();
    } else {
        document.addEventListener('DOMContentLoaded', initSearchAnimation);
    }
}
