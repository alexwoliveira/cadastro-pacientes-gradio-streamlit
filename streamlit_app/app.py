"""
Cadastro de Pacientes — versão Streamlit (deploy no Streamlit Community Cloud)
Atividade Prática Aula 1 — Aplicações em Data Science (prof. Francisco Fambrini)

Executar localmente:  streamlit run app.py
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]
ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.csv")
FUSO = ZoneInfo("America/Sao_Paulo")  # o servidor da nuvem roda em UTC

st.set_page_config(page_title="Cadastro de Pacientes", page_icon="🏥", layout="centered")
st.title("🏥 Cadastro de Pacientes")
st.caption("Recepção do consultório — registro rápido de chegada.")

# Acumula os pacientes da sessão
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)

with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox("Convênio", CONVENIOS)
    prioridade = st.slider("Prioridade do atendimento (5 = urgente)", 1, 5, 1)
    motivo = st.text_area("Motivo da consulta / observações")
    enviado = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)

if enviado:
    if not nome.strip():
        st.warning("Informe o nome do paciente.")
    else:
        nova_linha = {
            "timestamp": datetime.now(FUSO).strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo.strip(),
        }
        novo = pd.DataFrame([nova_linha], columns=COLUNAS)
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, novo], ignore_index=True
        )
        # Grava também em disco (mesma lógica da versão Gradio).
        # Atenção: no Streamlit Cloud esse disco é efêmero → use o botão de download.
        novo.to_csv(ARQUIVO_CSV, mode="a", header=not os.path.exists(ARQUIVO_CSV),
                    index=False, encoding="utf-8")
        st.success(f"Paciente {nova_linha['nome']} cadastrado!")

df = st.session_state.pacientes
st.subheader("Últimos pacientes cadastrados")
st.metric("Cadastros nesta sessão", len(df))
st.dataframe(df.tail(5), use_container_width=True, hide_index=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Baixar CSV", csv, "pacientes.csv", "text/csv",
                   disabled=df.empty, use_container_width=True)
st.info("O armazenamento do Streamlit Cloud é temporário: baixe o CSV antes de fechar a página.")
