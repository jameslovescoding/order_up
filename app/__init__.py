from flask import Flask
from .config import Config
from .routes import orders, session
from .models import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, Employee
from .util import ListConverter

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.converters['list'] = ListConverter
app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)
db.init_app(app)  # Configure the application with SQLAlchemy

login = LoginManager(app)
login.login_view = "session.login"

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))