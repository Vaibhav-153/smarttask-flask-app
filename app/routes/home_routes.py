from flask import Blueprint, render_template, session, redirect, url_for

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    # If user already logged in, go to dashboard
    if session.get("user_id"):
        return redirect(url_for("tasks.dashboard"))

    return render_template("home.html")
