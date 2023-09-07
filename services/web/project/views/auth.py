from flask import request, jsonify, render_template, redirect, url_for, session, Blueprint
from project.models import User, OnlineUsers
from datetime import datetime
from hashlib import sha256
from project import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        online_user = OnlineUsers.query.filter_by(username=username).first()
        ipaddress = request.headers.get('X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
        print(ipaddress)
        online_ip = OnlineUsers.query.filter_by(ipaddress=ipaddress).first()
        if not online_user:
            if not online_ip:
                if user and user.password == sha256(password.encode()).hexdigest():
                    db.session.add(OnlineUsers(username=user.username, ipaddress=ipaddress, logindatetime=datetime.utcnow()))
                    db.session.commit()
                    session["errorMessage"] = ""
                    session["successMessage"] = "Logged in Successfully!"
                    session["username"] = user.username
                    return redirect(url_for("user.list_users"))
                else:
                    session["errorMessage"] = "Invalid Credentials!"
                    session["successMessage"] = ""
            else:
                session["errorMessage"] = "IP Already Online!"
                session["successMessage"] = ""
        else:
            session["errorMessage"] = "Already Logged In!"
            session["successMessage"] = ""

    return render_template('login.html'), 200

@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        if not request.is_json:
            return jsonify(status="Missing JSON")
        username = request.json.get("username")
        user = OnlineUsers.query.filter_by(username=username).first()
    elif request.method == "GET":
        username = session["username"]
        user = OnlineUsers.query.filter_by(username=username).first()

    if user:
        session["errorMessage"] = ""
        session["successMessage"] = "Successfully Logged Out!"
        session["username"] = ""
        db.session.delete(user)
        db.session.commit()
        return redirect("/")

    return jsonify(status="not logged in yet")

@auth_bp.route("/onlineusers", methods=["GET"])
def online_users():
    if session["username"] == "":
        session["errorMessage"] = "You Need to Login First!"
        session["successMessage"] = ""
        return redirect(url_for("auth.login"))
    onlineusers = OnlineUsers.query.all()
    online_users = [
        {
            "username": user.username,
            "ipaddress": user.ipaddress,
            "logindatetime": user.logindatetime
        }
        for user in onlineusers
    ]
    return render_template("onlineusers.html", onlineusers=onlineusers)