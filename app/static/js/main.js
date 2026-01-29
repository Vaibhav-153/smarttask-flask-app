// ==============================
// DOM READY
// ==============================
document.addEventListener("DOMContentLoaded", function () {

    // ==============================
    // AUTO-HIDE FLASH MESSAGES
    // ==============================
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";

            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 12000); // ⏱️ 12 seconds (good for OTP demo)
    });


    // ==============================
    // DISABLE DOUBLE FORM SUBMIT
    // ==============================
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {
        form.addEventListener("submit", function () {
            const buttons = form.querySelectorAll(
                "button[type='submit'], input[type='submit']"
            );

            buttons.forEach(btn => {
                btn.disabled = true;

                if (btn.tagName === "BUTTON") {
                    btn.innerText = "Please wait...";
                }
            });
        });
    });

});


// ==============================
// CONFIRM DELETE (GLOBAL SAFETY)
// ==============================
function confirmDelete(message = "Are you sure you want to delete this?") {
    return confirm(message);
}


// ==============================
// PASSWORD VISIBILITY TOGGLE
// ==============================
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.type = input.type === "password" ? "text" : "password";
}
