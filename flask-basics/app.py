from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knowledge_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ----------------------------
# Models
# ----------------------------

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    author = db.relationship('User', backref=db.backref('entries', lazy=True))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ----------------------------
# Login Manager Setup
# ----------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----------------------------
# Routes
# ----------------------------

@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.date_created.desc()).all()
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

    # Only allow owner or admin to edit
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

    # Only allow owner or admin to delete
    if entry.author != current_user and not current_user.is_admin:
        flash("You don't have permission to delete this entry.", "danger")
        return redirect(url_for('index'))

    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted successfully!", "success")
    return redirect(url_for('index'))

# ----------------------------
# Auth Routes
# ----------------------------

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

# ----------------------------
# Create DB & Run App
# ----------------------------

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)