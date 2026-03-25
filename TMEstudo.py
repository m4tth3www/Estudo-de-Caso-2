import sys
import subprocess

# ======================
# INSTALAR DEPENDÊNCIAS
# ======================
def ensure(packages):
    import importlib
    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except Exception:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure(["dash", "plotly", "pandas"])

# ======================
# IMPORTS
# ======================
import statistics
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import webbrowser

# ======================
# DADOS DA PESQUISA
# ======================
dados = [1]*5 + [2]*6 + [4]*3 + [7]*3
df = pd.DataFrame({"horas": dados})

# Frequência
freq_df = df["horas"].value_counts().sort_index().reset_index()
freq_df.columns = ["horas", "freq"]

# ======================
# ESTATÍSTICAS
# ======================
media = statistics.mean(dados)
mediana = statistics.median(dados)
moda = statistics.mode(dados)

# ======================
# GRÁFICOS
# ======================

# 🔹 Gráfico de barras simples: horas estudadas x quantidade
x_labels = ['1 h', '2 h', '4 h', '7 h']
fig_bar = px.bar(
    x=x_labels,
    y=freq_df['freq'],
    title='Horas Estudadas vs Quantidade',
    labels={'x': 'Horas Estudadas', 'y': 'Quantidade'}
)

# 🔹 Gráfico de pizza
fig_pie = px.pie(
    freq_df,
    names='horas',
    values='freq',
    title='Distribuição Geral das Respostas'
)


# ======================
# APP DASH
# ======================
app = Dash(__name__)
app.title = "Pesquisa de Estudo"

CARD_STYLE = {
    "background": "#f6f8fb",
    "padding": "14px",
    "border-radius": "8px",
    "box-shadow": "0 2px 6px rgba(0,0,0,0.06)",
    "text-align": "center",
}

app.layout = html.Div(
    style={"font-family": "Segoe UI, Arial", "margin": "18px"},
    children=[

        html.H2("Análise da Pesquisa de Estudo"),

        html.P(
            "Pergunta: Quantas horas por semana você estuda fora da sala?",
            style={"color": "#555"}
        ),

        # Estatísticas
        html.Div(
            style={"display": "flex", "gap": "12px", "margin-bottom": "18px"},
            children=[

                html.Div(style=CARD_STYLE, children=[
                    html.Div("Média"),
                    html.H3(f"{media:.2f} h")
                ]),

                html.Div(style=CARD_STYLE, children=[
                    html.Div("Mediana"),
                    html.H3(f"{mediana} h")
                ]),

                html.Div(style=CARD_STYLE, children=[
                    html.Div("Moda"),
                    html.H3(f"{moda} h")
                ]),
            ],
        ),

        # Gráficos: barras + setores
        html.Div(
            style={"display": "grid", "grid-template-columns": "1fr 1fr", "gap": "12px", "margin-bottom": "18px"},
            children=[
                dcc.Graph(figure=fig_bar),
                dcc.Graph(figure=fig_pie),
            ],
        ),
    ],
)

# ======================
# EXECUÇÃO
# ======================
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/")
    app.run(debug=True)