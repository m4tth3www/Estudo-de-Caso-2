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
    labels={'x': 'Horas Estudadas', 'y': 'Quantidade'},
    color_discrete_sequence=['#3498db']
)
fig_bar.update_layout(
    plot_bgcolor='rgba(240, 245, 250, 0.5)',
    paper_bgcolor='white',
    font=dict(family="Arial, sans-serif", size=12, color="#2c3e50"),
    title_font_size=18,
    showlegend=False,
    hovermode='x unified'
)

# 🔹 Gráfico de pizza
fig_pie = px.pie(
    freq_df,
    names='horas',
    values='freq',
    title='Distribuição Geral',
    color_discrete_sequence=['#3498db', '#e74c3c', '#f39c12', '#2ecc71']
)
fig_pie.update_layout(
    paper_bgcolor='white',
    font=dict(family="Arial, sans-serif", size=12, color="#2c3e50"),
    title_font_size=18
)


# ======================
# APP DASH
# ======================
app = Dash(__name__)
app.title = "Estudo de Caso 2 - Análise de Dados"

# Estilos das cartas de estatísticas
CARD_STYLE_BASE = {
    "padding": "24px",
    "border-radius": "12px",
    "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.1)",
    "text-align": "center",
    "flex": "1",
    "transition": "all 0.3s ease",
    "border": "none",
}

CARD_MEDIA = {**CARD_STYLE_BASE, "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"}
CARD_MEDIANA = {**CARD_STYLE_BASE, "background": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"}
CARD_MODA = {**CARD_STYLE_BASE, "background": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"}

# CSS externo para melhor styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                color: #2c3e50;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
                box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 8px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.95;
                font-weight: 300;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            
            .stat-card {
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                text-align: center;
                color: white;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            }
            
            .stat-card-media {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            .stat-card-mediana {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            }
            
            .stat-card-moda {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            }
            
            .stat-label {
                font-size: 0.95em;
                opacity: 0.9;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 12px;
            }
            
            .stat-value {
                font-size: 2.5em;
                font-weight: 700;
                letter-spacing: -1px;
            }
            
            .charts-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 24px;
                margin-bottom: 40px;
            }
            
            .chart-card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                overflow: hidden;
                transition: box-shadow 0.3s ease;
            }
            
            .chart-card:hover {
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            }
            
            .dash-graph {
                padding: 20px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(
    children=[
        # Header
        html.Div(
            className="header",
            children=[
                html.H1("📊 Análise de Horas de Estudo"),
                html.P("Pesquisa: Quantas horas por semana você estuda fora da sala?")
            ]
        ),
        
        # Container principal
        html.Div(
            className="container",
            children=[
                # Cards de Estatísticas
                html.Div(
                    className="stats-grid",
                    children=[
                        html.Div(
                            className="stat-card stat-card-media",
                            children=[
                                html.Div(className="stat-label", children="Média"),
                                html.Div(className="stat-value", children=f"{media:.2f} h")
                            ]
                        ),
                        html.Div(
                            className="stat-card stat-card-mediana",
                            children=[
                                html.Div(className="stat-label", children="Mediana"),
                                html.Div(className="stat-value", children=f"{mediana} h")
                            ]
                        ),
                        html.Div(
                            className="stat-card stat-card-moda",
                            children=[
                                html.Div(className="stat-label", children="Moda"),
                                html.Div(className="stat-value", children=f"{moda} h")
                            ]
                        ),
                    ]
                ),
                
                # Gráficos
                html.Div(
                    className="charts-container",
                    children=[
                        html.Div(
                            className="chart-card",
                            children=[dcc.Graph(figure=fig_bar)]
                        ),
                        html.Div(
                            className="chart-card",
                            children=[dcc.Graph(figure=fig_pie)]
                        ),
                    ]
                ),
            ]
        )
    ]
)

# ======================
# EXECUÇÃO
# ======================
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/")
    app.run(debug=True)