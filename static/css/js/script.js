// Basic JS for interactivity (e.g., form validation)
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            inputs.forEach(input => {
                if (!input.value) {
                    alert('Please fill all required fields.');
                    e.preventDefault();
                }
            });
        });
    });
});