from flask import request, jsonify, render_template, redirect, url_for, session, Blueprint
from project.models import User, OnlineUsers
from project import db
import re

user_bp = Blueprint("user", __name__)

@user_bp.route("/list", methods=["GET"])
def list_users():
    if session["username"] == "":
        session["errorMessage"] = "You Need to Login First!"
        session["successMessage"] = ""
        return redirect(url_for("auth.login"))
        
    users = User.query.all()
    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "firstname": user.firstname,
            "middlename": user.middlename,
            "lastname": user.lastname,
            "email": user.email,
            "birthdate": user.birthdate
        }
        for user in users
    ]
    return render_template("dashboard.html", user_list=user_list)

@user_bp.route("/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        password = request.form["password"]
        email = request.form["email"]
        username = request.form["username"]
        firstname = request.form["firstname"]
        middlename = request.form["middlename"]
        lastname = request.form["lastname"]
        birthdate = request.form["birthdate"]
        if not username or not firstname or not middlename or not lastname or not birthdate:
            session["errorMessage"] = "Missing Input!"
            session["successMessage"] = ""
        elif len(password) < 8 or not re.match(r"^[A-Za-z0-9]+$", password):
            session["errorMessage"] = "Password must be at least 8 characters long and contain only [A-Za-z0-9] characters!"
            session["successMessage"] = ""
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            session["errorMessage"] = "Invalid email format!"
            session["successMessage"] = ""
        else:
            user = User.query.filter_by(username=username).first()
            user2 = User.query.filter_by(email=email).first()
            if user:
                session["errorMessage"] = "Username already exists!"
                session["successMessage"] = ""
            elif user2:
                session["errorMessage"] = "Email already registered!"
                session["successMessage"] = ""
            else:
                db.session.add(User(username=username, firstname=firstname, middlename=middlename, lastname=lastname, birthdate=birthdate, email=email, password=password))
                db.session.commit()
                session["errorMessage"] = ""
                session["successMessage"] = "Registered Successfully!"
                return redirect(url_for("auth.login"))
    return render_template("register.html")

@user_bp.route("/delete/<int:id>", methods=["POST"])
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    if user:
        if user.username != session["username"]:
            session["errorMessage"] = ""
            session["successMessage"] = "User Deleted Succesfully!"
            db.session.delete(user)
            db.session.commit()
        else:
            session["errorMessage"] = "You Cannot Delete Yourself!"
            session["successMessage"] = ""
    else:
        session["errorMessage"] = "User Does Not Exist!"
        session["successMessage"] = ""

    return redirect(url_for("user.list_users"))

@user_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update_user(id):
    print(id)
    if request.method == "POST":
        password = request.form["password"]
        email = request.form["email"]
        username = request.form["username"]
        firstname = request.form["firstname"]
        middlename = request.form["middlename"]
        lastname = request.form["lastname"]
        birthdate = request.form["birthdate"]

        user = User.query.filter_by(id=id).first()

        if user:
            if username != "":
                user.username = username
            if firstname != "":
                user.firstname = firstname
            if middlename != "":
                user.middlename = middlename
            if lastname != "":
                user.lastname = lastname
            if birthdate != "":
                user.birthdate = birthdate
            if email != "":
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    user.email = email
                else: 
                    session["errorMessage"] = "Invalid Email Format!"
                    session["successMessage"] = ""
            if password != "":
                if len(password) > 8 and re.match(r"^[A-Za-z0-9]+$", password):
                    user.password = password
                else: 
                    session["errorMessage"] = "Password must be at least 8 characters long and contain only [A-Za-z0-9] characters!"
                    session["successMessage"] = ""
            db.session.commit()
        else:
            session["errorMessage"] = "User Does Not Exist!"
            session["successMessage"] = ""

    return redirect(url_for("user.list_users"))