# Cadastro de Pacientes — Gradio x Streamlit

Atividade Prática Aula 1 — Aplicações em Data Science (UNICAMP) — prof. Francisco Fambrini

Sistema de cadastro de pacientes para a recepção de um consultório médico, implementado duas vezes
para comparar as bibliotecas **Gradio** (execução local) e **Streamlit** (publicado no Streamlit Community Cloud).

**App publicado:** https://SEU-APP.streamlit.app  ← substituir pelo link gerado no deploy

## Estrutura

```
├── gradio_app/
│   ├── app.py              # versão Gradio (gr.Blocks, grava pacientes.csv)
│   ├── pacientes.csv       # CSV de exemplo gerado nos testes
│   └── requirements.txt
├── streamlit_app/
│   ├── app.py              # versão Streamlit (st.form + session_state + download)
│   └── requirements.txt
├── prints/                 # capturas de tela (Gradio desktop/celular, Streamlit)
├── requirements.txt
└── README.md
```

## Campos do formulário

| Campo | Gradio | Streamlit |
|---|---|---|
| Nome do paciente | `gr.Textbox` | `st.text_input` |
| Idade | `gr.Number` (0–120) | `st.number_input` (0–120) |
| Convênio | `gr.Dropdown` | `st.selectbox` |
| Prioridade (1–5, 5 = urgente) | `gr.Slider` | `st.slider` |
| Motivo / observações | `gr.Textbox(lines=3)` | `st.text_area` |

Cada envio grava uma linha com `timestamp, nome, idade, convenio, prioridade, motivo`.

## Como rodar localmente

```bash
pip install -r requirements.txt

# Gradio → http://127.0.0.1:7860
cd gradio_app && python app.py
# (para abrir no celular na mesma rede Wi-Fi: python app.py --rede  → http://IP-DO-PC:7860)

# Streamlit → http://localhost:8501
cd streamlit_app && streamlit run app.py
```

## Deploy no Streamlit Community Cloud

1. Criar um repositório **público** no GitHub e enviar esta pasta inteira.
2. Acessar https://share.streamlit.io e entrar com a conta do GitHub.
3. **Create app** → selecionar o repositório, a branch `main` e o arquivo **`streamlit_app/app.py`**.
4. Aguardar o build e testar pelo link `*.streamlit.app` — também no celular.

## Comparação prática

| Aspecto | Gradio | Streamlit |
|---|---|---|
| Modelo de execução | Orientado a eventos: cada botão chama uma função | Script reexecutado do topo a cada interação |
| Estado | Dados persistidos no CSV local | `st.session_state` acumula a sessão |
| Formulário | Componentes soltos + `botao.click(...)` | `st.form` agrupa e envia tudo de uma vez |
| Persistência na nuvem | — (roda local; `share=True` gera link temporário de 72h) | Disco efêmero → exige `st.download_button` |
| Publicação | Local ou Hugging Face Spaces | Streamlit Community Cloud direto do GitHub |
| Ponto forte | Demos de modelos de ML, API automática | Dashboards e apps de dados com pouco código |

**Observação:** no Streamlit Cloud o servidor roda em UTC, por isso o timestamp usa o fuso `America/Sao_Paulo`.
