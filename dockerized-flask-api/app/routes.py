# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import app, db
from .models import User, Entry

@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_category = request.form['category']
        entry_content = request.form['content']

        new_entry = Entry(
            title=entry_title,
            category=entry_category,
            content=entry_content,
            user_id=current_user.id
        )
        db.session.add(new_entry)
        db.session.commit()
        flash("Entry added successfully!", "success")
        return redirect(url_for('index'))

    return render_template('add_entry.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = Entry.query.get_or_404(id)

    if entry.author != current_user and not current_user.is_admin:
        flash("You don't have permission to edit this entry.", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        entry.title = request.form['title']
        entry.category = request.form['category']
        entry.content = request.form['content']
        db.session.commit()
        flash("Entry updated successfully!", "success")
        return redirect(url_for('index'))

    return render_template('edit_entry.html', entry=entry)


@app.route('/delete/<int:id>')
@login_required
def delete_entry(id):
    entry = Entry.query.get_or_404(id)

    if entry.author != current_user and not current_user.is_admin:
        flash("You don't have permission to delete this entry.", "danger")
        return redirect(url_for('index'))

    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted successfully!", "success")
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')