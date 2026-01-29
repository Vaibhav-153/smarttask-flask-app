from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from app.extensions import db
from app.models.task import Task
from app.forms.task_forms import TaskForm
from app.utils.decorators import login_required, profile_required


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("/dashboard")
@login_required
@profile_required
def dashboard():
    user_id = session.get("user_id")

    pending_tasks = Task.query.filter_by(
        user_id=user_id,
        is_completed=False
    ).all()

    completed_tasks = Task.query.filter_by(
        user_id=user_id,
        is_completed=True
    ).all()

    form = TaskForm()

    return render_template(
        "tasks/dashboard.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        form=form
    )

@task_bp.route("/create", methods=["POST"])
@login_required
@profile_required
def create_task():
    form = TaskForm()
    user_id = session.get("user_id")

    if form.validate_on_submit():
        task = Task(
            user_id=user_id,
            title=form.title.data,
            description=form.description.data
        )

        db.session.add(task)
        db.session.commit()

        flash("Task added successfully", "success")

    return redirect(url_for("tasks.dashboard"))

@task_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
@profile_required
def edit_task(task_id):
    user_id = session.get("user_id")

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        flash("Task not found or unauthorized", "danger")
        return redirect(url_for("tasks.dashboard"))

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data

        db.session.commit()

        flash("Task updated successfully", "success")
        return redirect(url_for("tasks.dashboard"))

    return render_template(
        "tasks/dashboard.html",
        edit_task=task,
        form=form
    )

@task_bp.route("/toggle/<int:task_id>")
@login_required
@profile_required
def toggle_task(task_id):
    user_id = session.get("user_id")

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        flash("Unauthorized action", "danger")
        return redirect(url_for("tasks.dashboard"))

    task.is_completed = not task.is_completed
    db.session.commit()

    flash("Task status updated", "info")
    return redirect(url_for("tasks.dashboard"))

@task_bp.route("/delete/<int:task_id>")
@login_required
@profile_required
def delete_task(task_id):
    user_id = session.get("user_id")

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        flash("Unauthorized action", "danger")
        return redirect(url_for("tasks.dashboard"))

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully", "success")
    return redirect(url_for("tasks.dashboard"))

