from flask import Flask
from flask_migrate import Migrate
from models import TokenBlocklist, db
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_mail import Mail


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///commerce.db"

migrate = Migrate(app, db)
db.init_app(app)

app.config["MAIL_SERVER"]= 'smtp.gmail.com'
app.config["MAIL_PORT"]=587
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USE_SSL"]=False
app.config["MAIL_USERNAME"]="a44209581@gmail.com"
app.config["MAIL_PASSWORD"]="anto292003"
app.config["MAIL_DEFAULT_SENDER"]="a44209581@gmail.com"

mail = Mail(app)


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "a$Xz!2@#1pQz*7d9_lR$32!89qweT^2aU!"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
jwt = JWTManager(app)
jwt.init_app(app)


from views import *

app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(auth_bp)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None