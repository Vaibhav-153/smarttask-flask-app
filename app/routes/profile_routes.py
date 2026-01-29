from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from app.extensions import db
from app.models.profile import Profile
from app.forms.profile_forms import ProfileForm
from app.utils.decorators import login_required
from app.models.user import User
from app.models.task import Task

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

@profile_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_profile():
    user_id = session.get("user_id")

    # If profile already exists, do not allow re-creation
    existing_profile = Profile.query.filter_by(user_id=user_id).first()
    if existing_profile:
        return redirect(url_for("profile.view_profile"))

    form = ProfileForm()

    if form.validate_on_submit():
        profile = Profile(
            user_id=user_id,
            full_name=form.full_name.data,
            email=form.email.data,
            mobile=form.mobile.data,
            dob=form.dob.data,
            gender=form.gender.data,
            occupation=form.occupation.data
        )

        db.session.add(profile)
        db.session.commit()

        flash("Profile created successfully", "success")
        return redirect(url_for("tasks.dashboard"))

    return render_template("profile/create_profile.html", form=form)

@profile_bp.route("/view")
@login_required
def view_profile():
    user_id = session.get("user_id")

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        return redirect(url_for("profile.create_profile"))

    return render_template("profile/view_profile.html", profile=profile)

@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    user_id = session.get("user_id")

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        flash("Please create your profile first", "warning")
        return redirect(url_for("profile.create_profile"))

    form = ProfileForm(obj=profile)

    if form.validate_on_submit():
        profile.full_name = form.full_name.data
        profile.email = form.email.data
        profile.mobile = form.mobile.data
        profile.dob = form.dob.data
        profile.gender = form.gender.data
        profile.occupation = form.occupation.data

        db.session.commit()

        flash("Profile updated successfully", "success")
        return redirect(url_for("profile.view_profile"))

    return render_template("profile/edit_profile.html", form=form)

@profile_bp.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    user_id = session.get("user_id")

    # Delete tasks
    Task.query.filter_by(user_id=user_id).delete()

    # Delete profile
    Profile.query.filter_by(user_id=user_id).delete()

    # Delete user
    user = User.query.get(user_id)
    db.session.delete(user)

    db.session.commit()
    session.clear()

    flash("Your account has been permanently deleted.", "info")
    return redirect(url_for("home.home"))

