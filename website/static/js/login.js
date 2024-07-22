function close_flashed_message() {
    let elements = document.getElementsByClassName("danger");
    for(let i = 0; i < elements.length; i++){
        elements[i].style.opacity = '0';
        elements[i].style.transition = 'opacity 0.5s ease-in-out';
        
        // Set a timeout to remove the element after the transition
        setTimeout(function() {
            elements[i].style.display = 'none';
        }, 500); // Match the timeout duration with the transition duration
    }
}


togglePassword.addEventListener('click', function (e) {

        const togglePassword = document.querySelector('#togglePassword');
        const password = document.querySelector('#floatingPassword');

        // Alternar el tipo de input entre 'password' y 'text'
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        
        // Cambiar el icono del ojito
        this.innerHTML = type === 'password' ? '<i class="fa-regular fa-eye"></i>' : '<i class="fa-regular fa-eye-slash"></i>';
    });


function caret_click(){
        const message = document.getElementById('message');
        const error_info = document.getElementById('error_info');
        message.style.display = 'block';
        error_info.style.display='none'
    
    }
