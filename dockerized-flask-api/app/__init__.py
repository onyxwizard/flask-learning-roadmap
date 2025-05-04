# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os


# Get absolute path to root folder
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(
    __name__,
    template_folder=os.path.join(project_root, 'templates'),
    static_folder=os.path.join(project_root, 'static')
)
# Initialize Flask app
app = Flask(__name__,template_folder='../templates',static_folder='../static')
app.config.from_mapping(
    SECRET_KEY='your-secret-key-here',
    SQLALCHEMY_DATABASE_URI='sqlite:///knowledge_base.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_SECRET_KEY='your-jwt-secret-key-here',
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=5)
)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)
api = Api(app)

# Import login manager user loader
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context processor for year
from datetime import datetime

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

# Import models, routes, and API resources
from .routes import index, add_entry, edit_entry, delete_entry, login, logout, register
from .apis import ApiLoginResource, EntryListResource, EntryResource

# Register API resources
api.add_resource(ApiLoginResource, '/api/login')
api.add_resource(EntryListResource, '/api/entries')
api.add_resource(EntryResource, '/api/entries/<int:entry_id>')

# Create DB and seed admin on startup
with app.app_context():
    db.create_all()

    from .models import db, User
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin123')  # Change before production!
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")