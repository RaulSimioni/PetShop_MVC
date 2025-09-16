from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.model.models import db, User

auth_views_bp = Blueprint("auth_views", __name__)

@auth_views_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form["username"]
        password = request.form["password"]

        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and user.check_password(password):
            session["logged_in"] = True
            session["username"] = user.username
            session["user_id"] = user.id
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciais inválidas. Tente novamente.", "danger")
    return render_template("auth/login.html")

@auth_views_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("As senhas não coincidem.", "danger")
            return render_template("auth/register.html", username=username, email=email)

        if User.query.filter_by(username=username).first():
            flash("Nome de usuário já existe.", "danger")
            return render_template("auth/register.html", username=username, email=email)

        if User.query.filter_by(email=email).first():
            flash("Email já registrado.", "danger")
            return render_template("auth/register.html", username=username, email=email)

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registro bem-sucedido! Faça login para continuar.", "success")
        return redirect(url_for("auth_views.login"))
    return render_template("auth/register.html")

@auth_views_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    session.pop("user_id", None)
    flash("Você foi desconectado.", "info")
    return redirect(url_for("auth_views.login"))
