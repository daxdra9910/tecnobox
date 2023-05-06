const form = document.getElementById('signup_form');


function validate_birthdate(event) {
    // Valida que el usuario sea mayor de edad.
    const birthdate = document.getElementById('birthdate');
    const birthdateHelp = document.getElementById('birthdate-help');
    const today = new Date();
    const date = new Date(birthdate.value);
    const age = today.getFullYear() - date.getFullYear();

    if (age < 18) {
        birthdate.classList.add('invalid-field');
        birthdateHelp.innerText = 'Debes ser mayor de edad!';
        event.preventDefault();
    }
    else {
        birthdate.classList.remove('invalid-field');
        birthdateHelp.innerText = '';
    }
}


function validate_phone(event) {
    // Valida que el número de teléfono sea válido.
    const phone = document.getElementById('phone');
    const phoneHelp = document.getElementById('phone-help');
    const pattern = /^\d{10}$/;

    if (!pattern.test(phone.value) && phone.value !== '') {
        phone.classList.add('invalid-field');
        phoneHelp.innerHTML = 'Ingresa un número de teléfono válido, por favor.';
        event.preventDefault();
    }
    else {
        phone.classList.remove('invalid-field');
        phoneHelp.innerHTML = '';
    }
}


function validate_email(event) {
    // Valida que el correo electrónico sea válido.
    const email = document.getElementById('email');
    const emailHelp = document.getElementById('email-help');
    const pattern = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/;

    if (!pattern.test(email.value) && email.value !== '') {
        email.classList.add('invalid-field');
        emailHelp.innerHTML = 'Ingresa un correo electrónico válido, por favor.';
        event.preventDefault();
    }
    else {
        email.classList.remove('invalid-field');
        emailHelp.innerHTML = '';
    }
}


function validate_username(event) {
    // Valida que un nombre de usuario solo contenga caracteres alfanuméricos y guión bajo.
    const username = document.getElementById('username');
    const usernameHelp = document.getElementById('username-help');
    const pattern = /^\w+$/;

    if (!pattern.test(username.value) && username.value !== '') {
        username.classList.add('invalid-field');
        usernameHelp.innerHTML = 'Solo puede contener caracteres alfanuméricos y guión bajo.';
        event.preventDefault();
    }
    else {
        username.classList.remove('invalid-field');
        usernameHelp.innerHTML = '';
    }
}


function validate_password(event) {
    // Valida que la contraseña sea adecuada.
    const password1 = document.getElementById('password1');
    const password1Help = document.getElementById('password1-help');

    const pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/;
    if (!pattern.test(password1.value) && password1.value !== '') {
        password1.classList.add('invalid-field');
        password1Help.innerHTML = 'La contraseña no es válida. Debe tener al menos:<ul><li>8 caracteres.</li><li>Una letra mayúscula.</li><li>Una letra minúscula.</li><li>Un número.</li><li>Un carácter especial.</li></ul>';
        event.preventDefault();
    }
    else {
        password1.classList.remove('invalid-field');
        password1Help.innerHTML = '';
    }
}


function confirm_password(event) {
    // Valida que el campo contraseña y confirmar contraseñan tengan el mismo valor.
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const password2Help = document.getElementById('password2-help');

    if (password1.value !== password2.value) {
        password2.classList.add('invalid-field');
        password2Help.innerText = 'Las contraseñas no coinciden!';
        event.preventDefault();
    }
    else {
        password2.classList.remove('invalid-field');
        password2Help.innerText = '';
    }
}


function validate_terms_and_conditions(event) {
    // Lanza un mensaje de alerta si no se acepta la declaración de privacidad ni los términos y condiciones.
    const check1 = document.getElementById('check1');
    const check2 = document.getElementById('check2');

    if (!check1.checked || !check2.checked) {
        event.preventDefault();
        $('#myModal').modal('show');
    }
}


form.addEventListener('submit', validate_birthdate);
form.addEventListener('submit', validate_phone);
form.addEventListener('submit', validate_email);
form.addEventListener('submit', validate_username);
form.addEventListener('submit', validate_password);
form.addEventListener('submit', confirm_password);
form.addEventListener('submit', validate_terms_and_conditions);