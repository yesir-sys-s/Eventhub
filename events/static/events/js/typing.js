function typeText(element, text, speed = 100) {
    let index = 0;
    element.textContent = '';
    element.classList.add('typing-effect');
    
    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
        } else {
            // Optional: remove the blinking cursor when typing is complete
            // element.classList.remove('typing-effect');
        }
    }
    
    type();
}

document.addEventListener('DOMContentLoaded', function() {
    // Find all elements with data-type-text attribute
    document.querySelectorAll('[data-type-text]').forEach(element => {
        const text = element.dataset.typeText;
        typeText(element, text);
    });
});
