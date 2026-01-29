// ==============================
// AUTO-HIDE FLASH MESSAGES
// ==============================
setTimeout(function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 500);
    });
}, 3000);


// ==============================
// CONFIRM DELETE (GLOBAL SAFETY)
// ==============================
function confirmDelete(message = "Are you sure you want to delete this?") {
    return confirm(message);
}


// ==============================
// DISABLE DOUBLE FORM SUBMIT
// ==============================
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            const buttons = form.querySelectorAll("button[type='submit'], input[type='submit']");
            buttons.forEach(btn => {
                btn.disabled = true;
                btn.innerText = "Please wait...";
            });
        });
    });
});


// ==============================
// SIMPLE PASSWORD TOGGLE (OPTIONAL)
// ==============================
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.type = input.type === "password" ? "text" : "password";
}
