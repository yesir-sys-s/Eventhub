document.addEventListener('DOMContentLoaded', function() {
    const options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.2
    };

    const animations = [
        'fade-in',
        'fade-left',
        'fade-right',
        'scale-up'
    ];
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                // Find which animation class this element has
                const animation = animations.find(a => element.classList.contains(a));
                if (animation) {
                    element.classList.add(animation + '-visible');
                }
                observer.unobserve(element);
            }
        });
    }, options);

    // Observe all elements with animation classes
    animations.forEach(animation => {
        document.querySelectorAll('.' + animation).forEach(element => {
            observer.observe(element);
        });
    });
});
