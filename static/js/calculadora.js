document.addEventListener("keydown", function(event) {

    const tecla = event.key;

    let valor = null;
    let acao = null;

    // Números
    if (/^[0-9.]$/.test(tecla)) {
        valor = tecla;
    }

    // Operadores
    else if (["+", "-", "*", "/"].includes(tecla)) {
        valor = tecla;
    }

    // Porcentagem
    else if (tecla === "%") {
        valor = "%";
    }

    // Calcular
    else if (tecla === "Enter" || tecla === "=") {
        acao = "calcular";
    }

    // Apagar
    else if (tecla === "Backspace") {
        acao = "apagar";
    }

    // Limpar
    else if (tecla === "Escape") {
        acao = "limpar";
    }

    // Inverter sinal
    else if (tecla === "F9") {
        acao = "inverter";
    }

    else {
        return;
    }

    event.preventDefault();

    const formulario = document.querySelector(".teclado");

    const campo = formulario.querySelector('input[name="expressao"]');

    if (valor !== null) {
        campo.value += valor;
    }

    if (acao !== null) {
        const botao = document.createElement("button");

        botao.type = "submit";
        botao.name = "acao";
        botao.value = acao;

        formulario.appendChild(botao);
        botao.click();
    }

    else {
        formulario.requestSubmit();
    }

});
// ALTERNAR TEMA CLARO E ESCURO

const btnTema = document.getElementById("btnTema");

btnTema.addEventListener("click", function() {

    document.body.classList.toggle("tema-claro");

    if (document.body.classList.contains("tema-claro")) {
        btnTema.textContent = "☾";
    } else {
        btnTema.textContent = "☀";
    }

});