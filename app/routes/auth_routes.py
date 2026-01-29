from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)

from app.forms.auth_forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm
)

from app.models.user import User
from app.extensions import db

from app.services.auth_service import (
    create_user,
    authenticate_user,
    hash_password
)
from app.services.otp_service import generate_otp, store_otp, verify_otp
from app.services.notification_service import send_otp
from app.models.profile import Profile


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # ✅ Check username uniqueness FIRST
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already taken. Please choose another.", "danger")
            return render_template("auth/register.html", form=form)

        # ✅ Check email uniqueness (via profile)
        existing_profile = Profile.query.filter_by(email=form.email.data).first()
        if existing_profile:
            flash("An account with this email already exists. Please login.", "warning")
            return redirect(url_for("auth.login"))

        # Generate OTP
        otp = generate_otp()
        store_otp(otp)

        # Store temp data
        session["temp_user"] = {
            "username": form.username.data,
            "password": form.password.data,
            "email": form.email.data
        }

        send_otp(
            contact=form.email.data,
            method="email",
            otp=otp
        )

        flash("OTP sent to your email", "info")
        return redirect(url_for("auth.verify_otp_route"))

    return render_template("auth/register.html", form=form)


# =========================
# OTP VERIFICATION
# =========================
@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp_route():
    if request.method == "POST":
        user_otp = request.form.get("otp")

        if verify_otp(user_otp):
            temp_user = session.get("temp_user")

            if not temp_user:
                flash("Session expired. Please register again.", "danger")
                return redirect(url_for("auth.register"))

            create_user(
                username=temp_user["username"],
                password=temp_user["password"]
            )

            session.pop("temp_user", None)

            flash("Registration successful. Please login.", "success")
            return redirect(url_for("auth.login"))

        flash("Invalid or expired OTP", "danger")

    return render_template("auth/otp_verify.html")


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(
            form.username.data,
            form.password.data
        )

        # ❌ Invalid credentials
        if user is None:
            flash("Invalid username or password", "danger")
            return render_template("auth/login.html", form=form)

        # ✅ Valid login
        session.clear()
        session["user_id"] = user.id

        flash("Login successful", "success")
        return redirect(url_for("tasks.dashboard"))

    # GET request OR validation error
    return render_template("auth/login.html", form=form)

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        # ✅ Query PROFILE, not USER
        profile = Profile.query.filter_by(email=form.email.data).first()

        if not profile:
            flash("No account found with this email", "danger")
            return render_template("auth/forgot_password.html", form=form)

        # Generate OTP
        otp = generate_otp()
        store_otp(otp)

        # Store user id for reset
        session["reset_user_id"] = profile.user_id

        # Send OTP
        send_otp(
            contact=form.email.data,
            method="email",
            otp=otp
        )

        flash("OTP sent for password reset", "info")
        return redirect(url_for("auth.reset_password"))

    return render_template("auth/forgot_password.html", form=form)

@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    form = ResetPasswordForm()
    user_id = session.get("reset_user_id")

    if not user_id:
        flash("Session expired. Try again.", "warning")
        return redirect(url_for("auth.forgot_password"))

    if form.validate_on_submit():
        user_otp = request.form.get("otp")

        if not verify_otp(user_otp):
            flash("Invalid or expired OTP", "danger")
            return redirect(url_for("auth.reset_password"))

        user = User.query.get(user_id)
        user.password_hash = hash_password(form.password.data)

        db.session.commit()
        session.pop("reset_user_id", None)

        flash("Password reset successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", form=form)


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))
