document.querySelectorAll('.number-input').forEach((input, index, array) => {
    input.addEventListener('input', () => {
        if (input.value.length === 1 && index < array.length - 1) {
            array[index + 1].focus();
        }
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && input.value === '' && index > 0) {
            array[index - 1].focus();
        }
    });

    input.addEventListener('keypress', (e) => {
        if (!/[0-9]/.test(e.key)) {
            e.preventDefault();
        }
    });
});