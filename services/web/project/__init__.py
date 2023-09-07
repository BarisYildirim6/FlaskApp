from flask import Flask, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="abcdefgh"
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

from project.views.user import user_bp
from project.views.auth import auth_bp

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(auth_bp)

@app.route("/", methods=["GET"])
def splash():
    return redirect(url_for("auth.login"))