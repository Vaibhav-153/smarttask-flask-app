from functools import wraps
from flask import session, redirect, url_for, flash

from app.models.user import User
from app.models.profile import Profile


# =========================
# LOGIN REQUIRED DECORATOR
# =========================
def login_required(view_func):
    """
    Ensures that the user is logged in.
    If not logged in, redirects to login page.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")

        # User not logged in
        if not user_id:
            flash("Please login to continue.", "warning")
            return redirect(url_for("auth.login"))

        # Extra safety: user exists in DB
        user = User.query.get(user_id)
        if not user:
            session.clear()
            flash("Session expired. Please login again.", "warning")
            return redirect(url_for("auth.login"))

        return view_func(*args, **kwargs)

    return wrapper


# =========================
# PROFILE REQUIRED DECORATOR
# =========================
def profile_required(view_func):
    """
    Ensures that the logged-in user has completed their profile.
    If profile does not exist, redirects to profile creation page.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")

        profile = Profile.query.filter_by(user_id=user_id).first()

        if not profile:
            flash("Please complete your profile first.", "info")
            return redirect(url_for("profile.create_profile"))

        return view_func(*args, **kwargs)

    return wrapper
