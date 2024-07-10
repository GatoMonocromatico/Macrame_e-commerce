const sacola = $("#sacola_input")
const numero_de_itens_sacola = $("#numero_de_itens_sacola")
const barra_todos_produtos = $("#barra_produtos_tudo")
const form_corpo = $("#corpo_form")
var espacamento_entre_produtos = 0
var tamanho_cart_produto = 0
var dict_valores_de_recuo = {}

function mover_barra_produtos(id, direcao, num_produtos) {
    atualiza_valor_espacamento_produtos()
    let barra_produtos = $(`#${id}`)
    let num_carts_recuados
    if (id in dict_valores_de_recuo) {
        num_carts_recuados = dict_valores_de_recuo[id]
    } else {
        num_carts_recuados = 0
    }

    if (direcao == "esquerda") {
        num_carts_recuados += 1
    } else {
        num_carts_recuados -= 1
    }

    let valor_maximo = num_produtos - 3

    if (num_carts_recuados >= 0 && num_carts_recuados <= valor_maximo) {
        dict_valores_de_recuo[id] = num_carts_recuados

        let valor_modificar = tamanho_cart_produto + espacamento_entre_produtos 

        let valor_resultante = -(num_carts_recuados * valor_modificar)

        barra_produtos.css("transform", `translateX(${valor_resultante}px)`)
        $(`#valor_x_${id}`).val(valor_resultante)

        console.log(valor_resultante, valor_maximo)
    }

    
}

function adicionar_a_sacola(item) {
    let itens_ja_adicionados = sacola.val()
    if (!itens_ja_adicionados.includes(item)) {
        sacola.val(`${itens_ja_adicionados}|${item}|`)
        aumentar_num_itens_sacola()
    }
    console.log(sacola.val())
}

function aumentar_num_itens_sacola() {
    let numero_atual_de_itens = numero_de_itens_sacola.text()
    if (numero_atual_de_itens == "") {
        numero_atual_de_itens = 0 
    }

    numero_atual_de_itens = parseInt(numero_atual_de_itens) + 1

    numero_de_itens_sacola.html(numero_atual_de_itens)
}

document.addEventListener("DOMContentLoaded", inserir_produtos_no_documento())

function inserir_produtos_no_documento() {
        $.ajax({
            url: "/backend/get_products",
            type: "GET",
            success: function(data) {
                console.log(data)
                for (item in data) {
                    form_corpo.append(data[item])
                }
                atualiza_espacamento_produtos()
                muda_visibilidade_loading("hidden")
            },
            error: function(erro) {
                console.log(erro)
            }
     })
}

function muda_visibilidade_loading(visibilidade) {
    $("#background_loading").css("visibility", visibilidade)
    $("#img_loading").css("visibility", visibilidade)
}

async function atualiza_espacamento_produtos() {
    await sleep(200)
    let valor_antigo_espacamento = espacamento_entre_produtos
    atualiza_valor_espacamento_produtos()
    $(".produto").css("margin-right", espacamento_entre_produtos)

    if (valor_antigo_espacamento != 0) {
        for (id in dict_valores_de_recuo) {
            let num_carts_recuados = dict_valores_de_recuo[id]
            let valor_modificar = tamanho_cart_produto + espacamento_entre_produtos 
            let valor_resultante = -(num_carts_recuados * valor_modificar)

            $(`#${id}`).css("transform", `translateX(${valor_resultante}px)`)
        }
    }
}

function atualiza_valor_espacamento_produtos() {
    tamanho_cart_produto = parseFloat($(".produto").css("width").replace("px"))
    let largura_container_produtos = parseFloat($(".produtos").css("width").replace("px", ""))

    
    espacamento_entre_produtos = (largura_container_produtos-(3*tamanho_cart_produto))/2
    if (espacamento_entre_produtos <= 0) {
        espacamento_entre_produtos = (largura_container_produtos-(2*tamanho_cart_produto))
    }
}

const sleep = ms => new Promise(r => setTimeout(r, ms))

window.onresize = function () {
    atualiza_espacamento_produtos()
    $("body").css("height", window.innerHeight)
    $("body").css("max-height", window.innerHeight)
    $("body").css("width", window.innerHeight)
    $("body").css("max-width", window.innerHeight)
}