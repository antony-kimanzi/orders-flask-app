from flask import Flask
from flask_migrate import Migrate
from models import db
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///commerce.db"

migrate = Migrate(app, db)
db.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "a$Xz!2@#1pQz*7d9_lR$32!89qweT^2aU!"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
jwt = JWTManager(app)
jwt.init_app(app)


from views import *

app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(auth_bp)