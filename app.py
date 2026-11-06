from flask import Flask, render_template, request
import ast
import operator
import re
import math

app = Flask(__name__)


# Operações matemáticas permitidas
operacoes = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}


# Interpretar expressão matemática
def calcular_expressao(expressao):

    # Converter porcentagem em divisão por 100
    expressao = re.sub(
        r'(\d+(?:\.\d+)?)%',
        r'(\1/100)',
        expressao
    )

    arvore = ast.parse(expressao, mode="eval")

    def interpretar(no):

        if isinstance(no, ast.Expression):
            return interpretar(no.body)

        if isinstance(no, ast.Constant) and type(no.value) in (int, float):
            return no.value

        if isinstance(no, ast.BinOp):

            tipo_operacao = type(no.op)

            if tipo_operacao not in operacoes:
                raise ValueError("Operação não permitida")

            esquerda = interpretar(no.left)
            direita = interpretar(no.right)

            return operacoes[tipo_operacao](esquerda, direita)

        if isinstance(no, ast.UnaryOp):

            valor = interpretar(no.operand)

            if isinstance(no.op, ast.USub):
                return -valor

            if isinstance(no.op, ast.UAdd):
                return valor

        raise ValueError("Expressão inválida")

    resultado = interpretar(arvore)

    if not isinstance(resultado, (int, float)) or not math.isfinite(resultado):
        raise ValueError("Resultado inválido")

    return resultado


# Página principal e processamento dos botões
@app.route("/", methods=["GET", "POST"])
def index():

    expressao = ""
    resultado = None
    erro = ""

    if request.method == "POST":

        expressao = request.form.get("expressao", "")
        valor = request.form.get("valor")
        acao = request.form.get("acao")

        try:

            if acao == "limpar":
                expressao = ""

            elif acao == "apagar":
                expressao = expressao[:-1]

            elif acao == "inverter":
                correspondencia = re.search(r'(\d+(?:\.\d+)?)$', expressao)

                if correspondencia:
                    numero = correspondencia.group(1)
                    inicio = expressao[:-len(numero)]

                    if inicio.endswith("-"):
                        expressao = inicio[:-1] + numero
                    else:
                        expressao = inicio + "-" + numero

            elif acao == "calcular":

                if not expressao:
                    raise ValueError("Digite uma operação.")

                if not re.fullmatch(r"[0-9+\-*/().% ]+", expressao):
                    raise ValueError("Expressão inválida.")

                resultado = calcular_expressao(expressao)

                expressao = str(resultado)

            elif valor is not None:

                if len(expressao) < 100:
                    expressao += valor

        except ZeroDivisionError:
            erro = "Não é possível dividir por zero."

        except Exception:
            erro = "Não foi possível realizar o cálculo."

    return render_template(
        "index.html",
        expressao=expressao,
        resultado=resultado,
        erro=erro
    )


if __name__ == "__main__":
    app.run(debug=True)