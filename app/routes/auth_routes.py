from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)
import time

from app.forms.auth_forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm
)

from app.models.user import User
from app.models.profile import Profile
from app.extensions import db

from app.services.auth_service import (
    create_user,
    authenticate_user,
    hash_password
)

from app.services.otp_service import generate_otp

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        # ✅ Username uniqueness
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken. Please choose another.", "danger")
            return render_template("auth/register.html", form=form)

        # ✅ Email uniqueness (profile-based)
        if Profile.query.filter_by(email=form.email.data).first():
            flash("An account with this email already exists. Please login.", "warning")
            return redirect(url_for("auth.login"))

        # ✅ Generate OTP
        otp = generate_otp()

        # ✅ Store OTP in session (DEMO MODE)
        session["otp"] = otp
        session["otp_expires"] = time.time() + 300  # 5 minutes
        session["otp_email"] = form.email.data

        # ✅ Temporarily store user data
        session["temp_user"] = {
            "username": form.username.data,
            "password": form.password.data,
            "email": form.email.data
        }

        # ✅ FLASH OTP (DEMO MODE)
        flash(
            f"[DEMO MODE] Your OTP is {otp}. This is shown only for demo purposes.",
            "info"
        )

        return redirect(url_for("auth.verify_otp_route"))

    return render_template("auth/register.html", form=form)


# =========================
# OTP VERIFICATION
# =========================
@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp_route():
    if request.method == "POST":
        user_otp = request.form.get("otp")

        stored_otp = session.get("otp")
        expires_at = session.get("otp_expires")

        if not stored_otp or time.time() > expires_at:
            flash("OTP expired. Please try again.", "danger")
            return redirect(url_for("auth.register"))

        if str(user_otp) != str(stored_otp):
            flash("Invalid OTP", "danger")
            return redirect(url_for("auth.verify_otp_route"))

        temp_user = session.get("temp_user")
        if not temp_user:
            flash("Session expired. Please register again.", "danger")
            return redirect(url_for("auth.register"))

        # ✅ Create user
        create_user(
            username=temp_user["username"],
            password=temp_user["password"]
        )

        # ✅ Clear OTP & temp data
        session.pop("temp_user", None)
        session.pop("otp", None)
        session.pop("otp_expires", None)
        session.pop("otp_email", None)

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

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

        if user is None:
            flash("Invalid username or password", "danger")
            return render_template("auth/login.html", form=form)

        session.clear()
        session["user_id"] = user.id

        flash("Login successful", "success")
        return redirect(url_for("tasks.dashboard"))

    return render_template("auth/login.html", form=form)


# =========================
# FORGOT PASSWORD
# =========================
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        profile = Profile.query.filter_by(email=form.email.data).first()

        if not profile:
            flash("No account found with this email", "danger")
            return render_template("auth/forgot_password.html", form=form)

        otp = generate_otp()

        # ✅ Store OTP in session
        session["otp"] = otp
        session["otp_expires"] = time.time() + 300
        session["reset_user_id"] = profile.user_id

        # ✅ FLASH OTP (DEMO MODE)
        flash(
            f"[DEMO MODE] Your OTP is {otp}. This is shown only for demo purposes.",
            "info"
        )

        return redirect(url_for("auth.reset_password"))

    return render_template("auth/forgot_password.html", form=form)


# =========================
# RESET PASSWORD
# =========================
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    form = ResetPasswordForm()
    user_id = session.get("reset_user_id")

    if not user_id:
        flash("Session expired. Try again.", "warning")
        return redirect(url_for("auth.forgot_password"))

    if form.validate_on_submit():
        user_otp = request.form.get("otp")

        stored_otp = session.get("otp")
        expires_at = session.get("otp_expires")

        if not stored_otp or time.time() > expires_at:
            flash("OTP expired. Please try again.", "danger")
            return redirect(url_for("auth.forgot_password"))

        if str(user_otp) != str(stored_otp):
            flash("Invalid OTP", "danger")
            return redirect(url_for("auth.reset_password"))

        user = User.query.get(user_id)
        user.password_hash = hash_password(form.password.data)

        db.session.commit()

        session.pop("reset_user_id", None)
        session.pop("otp", None)
        session.pop("otp_expires", None)

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
