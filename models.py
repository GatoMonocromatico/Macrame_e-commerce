from flask_login import UserMixin
from config import bd
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField


class User(UserMixin):
    def __init__(self, dados, usuario_novo):
        self.id = dados["id"]
        self.email = dados["email"]
        self.senha = dados["senha_hash"]
        self.nome = dados["nome"]

        if usuario_novo:
            bd.child(f"usuarios/{self.id}").set(dados)


def carrega_usuario(user_id):
    dados_usuario = bd.child(f"usuarios/{user_id}").get().val()
    if dados_usuario:
        return User(dados_usuario, False)
    else:
        return None


class FormCarrinhoComprasIndex(FlaskForm):
    pass


class FormCarrinhoCompras(FlaskForm):
    pass