from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash


# Criação do Blueprint
from config import bd, auth_firebase
from models import User
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            modalidade = request.form["modalidade"]
            email = request.form['email']
            senha = request.form['senha']

            if modalidade == "registrar":
                nome = request.form["nome"]
                try:
                    user = auth_firebase.create_user_with_email_and_password(email, senha)
                    user_id = user['localId']
                    hashed_password = generate_password_hash(senha)
                    dados = {
                        "email": email,
                        "senha_hash": hashed_password,
                        "nome": nome,
                        "id": user_id
                    }
                    user_obj = User(dados, True)
                    login_user(user_obj)
                    return "registrado"
                except Exception as e:
                    return f"erro ao registrar: {e}", 400
            else:
                try:
                    user = auth_firebase.sign_in_with_email_and_password(email, senha)
                    user_id = user['localId']
                    dados = bd.child(f"usuarios/{user_id}").get().val()
                    if dados:
                        user_obj = User(dados, False)
                        login_user(user_obj)
                        return "logado"
                except Exception as e:
                    return f"erro ao logar: {e}", 400
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))