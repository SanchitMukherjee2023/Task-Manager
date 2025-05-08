from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .models import Task
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

@main.route('/add', methods=['POST'])
@login_required
def add_task():
    content = request.form.get('content')
    if content:
        task = Task(content=content, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return "Unauthorized", 403
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.dashboard'))
