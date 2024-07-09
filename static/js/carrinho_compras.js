const lista_de_itens = $("#lista_itens")
const soma_produtos_valores = $("#soma_produtos_valores")
const soma_produtos_nomes = $("#soma_produtos_nomes")
const valor_da_compra_texto = $("#valor_da_compra_texto")
const form = $("#form")
const input_telefone = $("#input_telefone")
const span_erro = $("#input_telefone_erro")
const label_input_telefone = $("#label_input_telefone")
const imagem_sacola_vazia = $("#img_sacola_vazia")
const info_bruta_itens_lista = $("#itens_sacola").val()
const btn_finalizar_compra = $("#btn_comprar")

function redirecionar_para_index() {
    window.location.href = "http://127.0.0.1:5000/"
}

function modificar_quantidade(item_index, quantidade_a_modificar, valor_maximo) {
    let text_qtd = $(`#lista_qtd_${item_index}`)
    let valor_atual = text_qtd.val()
    let valor_modificado = parseInt(valor_atual) + parseInt(quantidade_a_modificar)
    let desc_max = $(`#qtd_maximo_lista_${item_index}`)

    if (valor_modificado >= 1 && valor_modificado < valor_maximo) {
        desc_max.css("visibility", "hidden")
        text_qtd.val(valor_modificado)
        console.log(1)
    }
    else if (valor_modificado == valor_maximo) {
        desc_max.css("visibility", "visible")
        text_qtd.val(valor_modificado)
    }
}

function excluir_item(item_index) {
    let item = document.getElementById(`item_lista_${item_index}`)
    let nome_na_soma_valor = document.getElementById(`soma_produtos_nome_${item_index}`)
    let valor_na_soma = document.getElementById(`soma_produtos_valor_${item_index}`)
    let valor_total_compra_elemento = document.getElementById("valor_da_compra_texto")

    let valor_total_compra = parseInt(valor_total_compra_elemento.innerHTML.replace("R$ ", ""))
    let valor_do_item = parseInt(valor_na_soma.innerHTML.replace("R$ ", ""))
    let valor_resultante = valor_total_compra - valor_do_item

    item.parentNode.removeChild(item)
    nome_na_soma_valor.parentNode.removeChild(nome_na_soma_valor)
    valor_na_soma.parentNode.removeChild(valor_na_soma)

    valor_total_compra_elemento.innerHTML = `R$ ${valor_resultante},00`

    if (lista_de_itens.html().replaceAll("\n", "").replaceAll(" ", "") == "") {
        imagem_sacola_vazia.css("visibility", "visible")
        btn_finalizar_compra.attr("disabled", "disabled")
        $("#disclaimer_endereço").css("visibility", "hidden")
    }
} 

document.addEventListener("DOMContentLoaded", muda_visibilidade_loading("hidden"))
function muda_visibilidade_loading(visibilidade) {
    $("#background_loading").css("visibility", visibilidade)
    $("#img_loading").css("visibility", visibilidade)
}

form.on("submit", function(event) {
    let padrao_telefone = /\(?\d{2}\)?\s?9\d{4}-?\d{4}/
    let celular = input_telefone.val()

    if (!celular.match(padrao_telefone)) {
        event.preventDefault()
        span_erro.css("visibility", "visible")
        span_erro.css("animation", "piscar 450ms linear forwards")
        label_input_telefone.css("animation", "piscar 450ms linear forwards")
    }
})

$(".logo_frase").on("click", function() {
    window.location.href = "/"
})
