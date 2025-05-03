from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knowledge_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key-here'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)  # 👈 Set expiry here
jwt = JWTManager(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

api = Api(app)

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}


# ----------------------------
# Models
# ----------------------------

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------------------
# API Resources
# ----------------------------

entry_parser = reqparse.RequestParser()
entry_parser.add_argument('title', required=True)
entry_parser.add_argument('category', required=True)
entry_parser.add_argument('content', required=True)
entry_parser.add_argument('user_id', type=int, required=True)


class ApiLoginResource(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            claims = {"is_admin": user.is_admin}
            access_token = create_access_token(identity=user.username, additional_claims=claims)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid username or password'}, 401


class EntryListResource(Resource):
    @jwt_required()
    def get(self):
        entries = Entry.query.all()
        return [{
            'id': e.id,
            'title': e.title,
            'category': e.category,
            'content': e.content
        } for e in entries]

    @jwt_required()
    def post(self):
        data = entry_parser.parse_args()
        user = User.query.get(data['user_id'])
        if not user:
            return {'message': 'User not found'}, 404

        new_entry = Entry(**data)
        db.session.add(new_entry)
        db.session.commit()
        return {'message': 'Entry created', 'id': new_entry.id}, 201


class EntryResource(Resource):
    @jwt_required()
    def get(self, entry_id):
        entry = Entry.query.get_or_404(entry_id)
        return {
            'id': entry.id,
            'title': entry.title,
            'category': entry.category,
            'content': entry.content
        }

    @jwt_required()
    def put(self, entry_id):
        data = entry_parser.parse_args()
        entry = Entry.query.get_or_404(entry_id)
        entry.title = data['title']
        entry.category = data['category']
        entry.content = data['content']
        db.session.commit()
        return {'message': 'Entry updated'}

    @jwt_required()
    def delete(self, entry_id):
        entry = Entry.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()
        return {'message': 'Entry deleted'}


# Register API routes
api.add_resource(ApiLoginResource, '/api/login')
api.add_resource(EntryListResource, '/api/entries')
api.add_resource(EntryResource, '/api/entries/<int:entry_id>')


# ----------------------------
# Web Routes
# ----------------------------

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


# ----------------------------
# Create DB & Run App
# ----------------------------

with app.app_context():
    db.create_all()

    # Optional: Seed admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin123')  # Change this before production!
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

if __name__ == '__main__':
    app.run(debug=True)