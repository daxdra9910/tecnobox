function show_password(id, idBtn) {
    // Mostrar/Ocultar contraseña.
    const password = document.getElementById(id);
    const showPassword = document.getElementById(idBtn);

    if (password.type === "password") {
        password.type = "text";
        showPassword.innerHTML = '<i class="fas fa-eye"></i>';
    } else {
        password.type = "password";
        showPassword.innerHTML = '<i class="fas fa-eye-slash"></i>';
    }
}