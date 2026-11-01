"""
Cadastro de Pacientes — versão Gradio (execução local)
Atividade Prática Aula 1 — Aplicações em Data Science (prof. Francisco Fambrini)

Executar:  python app.py   → abre em http://127.0.0.1:7860
Para testar no celular (mesma rede Wi-Fi): python app.py --rede
"""
import os
import sys
from datetime import datetime

import gradio as gr
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA, "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]


def carregar_ultimos(n: int = 5) -> pd.DataFrame:
    """Lê o CSV (se existir) e devolve os últimos n cadastros."""
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(n)
    return pd.DataFrame(columns=COLUNAS)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    # --- validações simples ---
    nome = (nome or "").strip()
    if not nome:
        return "⚠️ Informe o nome do paciente.", carregar_ultimos()
    if idade is None or idade < 0 or idade > 120:
        return "⚠️ Informe uma idade válida (0 a 120).", carregar_ultimos()
    if not convenio:
        return "⚠️ Selecione o convênio.", carregar_ultimos()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": (motivo or "").strip(),
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    # cria o arquivo com cabeçalho na 1ª execução; depois só acrescenta linhas
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8")
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False, encoding="utf-8")

    total = len(pd.read_csv(ARQUIVO_CSV))
    msg = f"✅ Paciente {nome} cadastrado com sucesso! (total: {total})"
    return msg, carregar_ultimos()


def limpar():
    return "", "", None, None, 1, ""


# Layout em coluna única → usável em tela de celular
with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## 🏥 Cadastro de Pacientes\nRecepção do consultório — registro rápido de chegada.")

    with gr.Column():
        nome = gr.Textbox(label="Nome do paciente", placeholder="Ex.: Maria da Silva")
        idade = gr.Number(label="Idade", minimum=0, maximum=120, precision=0)
        convenio = gr.Dropdown(CONVENIOS, label="Convênio")
        prioridade = gr.Slider(1, 5, step=1, value=1,
                               label="Prioridade do atendimento (5 = urgente)")
        motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)

        botao = gr.Button("Cadastrar", variant="primary")
        botao_limpar = gr.Button("Limpar formulário")

        saida_msg = gr.Textbox(label="Status", interactive=False)
        tabela = gr.Dataframe(value=carregar_ultimos(), label="Últimos pacientes cadastrados",
                              interactive=False, wrap=True)

    botao.click(cadastrar_paciente,
                [nome, idade, convenio, prioridade, motivo],
                [saida_msg, tabela])
    botao_limpar.click(limpar, None, [saida_msg, nome, idade, convenio, prioridade, motivo])


if __name__ == "__main__":
    # "--rede" expõe o app na rede local para acessar pelo celular (http://IP-DO-PC:7860)
    demo.launch(server_name="0.0.0.0" if "--rede" in sys.argv else "127.0.0.1")
