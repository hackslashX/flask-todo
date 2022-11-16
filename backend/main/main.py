""" Entrypoing for the backend. """

from flask import Flask
from flask_jwt_extended import JWTManager

from app.api.v1.auth import auth_blueprint
from app.api.v1.tag import tag_blueprint
from app.api.v1.task import task_blueprint
from app.api.v1.user import user_blueprint
from app.core.config import settings

app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
app.register_blueprint(user_blueprint, url_prefix="/api/v1/")
app.register_blueprint(tag_blueprint, url_prefix="/api/v1/")
app.register_blueprint(task_blueprint, url_prefix="/api/v1/")

# Configure JWT
app.config["JWT_SECRET_KEY"] = settings.jwt.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.jwt.JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.jwt.JWT_REFRESH_TOKEN_EXPIRES

jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
