from flask import render_template, request, jsonify
import smtplib
import email.message
from config import app, bd, storage, csrf, login_manager, senha_gmail
from models import carrega_usuario, FormCarrinhoComprasIndex, FormCarrinhoCompras
import re

login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.user_loader(carrega_usuario)

from auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')


@app.route("/", methods=["POST", "GET"])
def index():
    form = FormCarrinhoComprasIndex()
    return render_template("index.html", form=form)


@app.route("/carrinho", methods=["POST", "GET"])
def carrinho():
    form = FormCarrinhoCompras()

    dados_return = {}
    soma_total = 0
    sacola_return = ""

    try:
        sacola = request.form["sacola"]
    except KeyError:
        sacola = ""

    if sacola != "":
        sacola = sacola.replace("||", ", ").replace("|", "")

        sacola_return = sacola

        sacola = sacola.split(", ")

        for item in sacola:
            dados_produto = bd.child(f"produtos/{item.lower()}").get().val()
            dados_produto["quantidade_unica"] = " quantidade_unica"
            soma_total += dados_produto["valor"]

            dados_produto["valor"] = retorna_str_numerico_2_digitos_pos_ponto(dados_produto["valor"])
            dados_return[item.capitalize()] = dados_produto

    soma_total = retorna_str_numerico_2_digitos_pos_ponto(soma_total)

    return render_template("carrinho_compras.html", itens=dados_return, form=form, soma_total=soma_total, sacola=sacola_return)


@app.route("/backend/calcula_valor_total")
def calcula_valor_total():
    valores = request.get_json()

    valor_total = valores["valor_total"]
    modificacao = valores["modificacao"]

    valor_return = valor_total + modificacao
    valor_return = retorna_str_numerico_2_digitos_pos_ponto(valor_return)

    return valor_return


def retorna_str_numerico_2_digitos_pos_ponto(soma_total):
    soma_total = str(soma_total).replace(",", ".")
    if "." not in soma_total:
        soma_total += '.00'
    elif re.fullmatch(r"\d+\.\d\d\d+", soma_total):
        soma_total = soma_total[:soma_total.find(".")+3]
    else:
        while not re.fullmatch(r"\d+\.\d\d", soma_total):
            soma_total += "0"

    return soma_total.replace(".", ",")


@app.route("/encomenda_realizada", methods=["POST"])
def encomenda_realizada():
    dados = request.form

    corpo_email = f"""
        <p>Você recebeu um novo pedido:</p>
        <p>Itens da encomenda: {dados["itens"]}</p>
        <p>Endereço fornecido: {dados["endereço"]}</p>
        <p>Telefone fornecido: {dados["telefone"]}</p>
        """

    msg = email.message.Message()
    msg['Subject'] = "Pedido recebido no site ecológica"
    msg['From'] = 'ivoarpino2@gmail.com'
    msg['To'] = 'ivoarpino2@gmail.com'
    password = senha_gmail
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

    return render_template("encomenda_realizada.html")


@app.route("/backend/get_products", methods=["GET", "POST"])
def get_products():
    categorias = bd.child("categorias").get().val()
    produtos = bd.child("produtos").get().val()

    dados_HTML = []

    for categoria in categorias:
        dados_categoria = {
            "produtos_da_categoria": {},
            "num_de_produtos": 0,
            "id_produtos": f"produtos_{categoria}",
            "id_div_barra_produtos": f"barra_produtos_{categoria}",
            "label": categoria.capitalize().replace("_", " ")

        }
        HTML_produtos = ""
        for produto in produtos:
            dados_produto = produtos[produto]

            if categoria == "todos_os_produtos":
                dados_produto["label"] = produto.capitalize()

                dados_categoria["num_de_produtos"] += 1
                dados_categoria["produtos_da_categoria"][produto] = dados_produto
            elif dados_produto["tipo"] == categoria:
                dados_produto["label"] = produto.capitalize()

                dados_categoria["num_de_produtos"] += 1
                dados_categoria["produtos_da_categoria"][produto] = dados_produto

        index_for = 0
        for produto in dados_categoria["produtos_da_categoria"]:
            dados_produto = dados_categoria["produtos_da_categoria"][produto]
            dados_produto["valor"] = retorna_str_numerico_2_digitos_pos_ponto(dados_produto["valor"])

            HTML_produtos += f'''\n<div class="produto">
                    <img draggable="false" class="imagem_demonstração" src="static/{dados_produto["img"]}.png">
                    <span class="texto_produto">{dados_produto["label"]}</span>
                    <span class="desc_tamanho">Tamanho {dados_produto["tamanho"]}</span>
                    <span class="valor">R$ {dados_produto["valor"]}</span>
                    <button class="btn_comprar" onclick="adicionar_a_sacola('{produto}')" type="button">Comprar</button>
                    </div>'''
            index_for += 1

        repeticao_de_produtos = 1 if index_for >= 3 else 4 - index_for

        HTML_estrutura = f'''
        <div id="{dados_categoria["id_div_barra_produtos"]}" class="barra_produtos">
            <span class="categoria_produtos" id="categoria_{dados_categoria["id_produtos"]}">{dados_categoria["label"]}</span>
            <div class="setas_com_produtos">
                <span class="tapa-luz"></span>
                <div class="seta seta_esquerda" onclick="mover_barra_produtos('{dados_categoria["id_produtos"]}', 'direita', {dados_categoria["num_de_produtos"]*repeticao_de_produtos})">
                    <span class="seta_span seta_span_esquerda"></span>
                </div>
                <div id="{dados_categoria["id_produtos"]}" class="produtos">
                {HTML_produtos*repeticao_de_produtos}
                </div>
                <div class="seta seta_direita" onclick="mover_barra_produtos('{dados_categoria["id_produtos"]}', 'esquerda', {dados_categoria["num_de_produtos"]*repeticao_de_produtos})">
                    <span class="seta_span seta_span_direita"></span>
                </div>
                <span class="tapa-luz"></span>
            </div>
        </div>
        '''

        dados_HTML.append(HTML_estrutura)

    return jsonify(dados_HTML)


if __name__ == "__main__":
    app.run(debug=True)
