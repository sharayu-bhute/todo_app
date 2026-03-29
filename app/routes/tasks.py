from flask import Flask, Blueprint, request, redirect, url_for, render_template, flash, session
from app import db
from app.models import Task

task_bp = Blueprint('task', __name__)

@task_bp.route('/')
def view_tasks():
    if 'user' not in session:
        flash('Please login to view tasks', 'warning')
        return redirect(url_for('auth.login'))
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@task_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        flash("Please login to add tasks", 'warning')
        return redirect(url_for('auth.login'))
    title = request.form.get('title')
    if title:
        new_task= Task(title=title)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
    return redirect(url_for('task.view_tasks'))

@task_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task= Task.query.get(task_id)
    if task:
        if task.status == 'pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'pending'
        db.session.commit()
        flash('Task status updated', 'success')
    return redirect(url_for('task.view_tasks'))

@task_bp.route('/clear',methods=['POST'])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared', 'success')
    return redirect(url_for('task.view_tasks'))

@task_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully', 'success')
    return redirect(url_for('task.view_tasks'))