"""Bibliotecas Necessárias"""
import dataclasses
import dash_bootstrap_components as dbc
from dash import dash_table, Dash, html
import pandas as pd
from model import ModeloPreditivo

@dataclasses.dataclass
class PrepararDados:
    """Melhorar a sintaxe dos Dados"""
    def __init__(self):
        modelo = ModeloPreditivo()
        modelo.adicionando_solucao()
        self.dados = modelo.jogos()
        self.dados_tabela = self.dados.copy()
        self.arredondar_colunas()
        self.excluir_colunas()
        self.porcentagem()
        self.selecionar_datas()

    def arredondar_colunas(self):
        """Arredonda colunas específicas do DataFrame"""
        self.dados_tabela['Prevision Home'] = self.dados_tabela['Prevision Home'].round(2)
        self.dados_tabela['Prevision Visitor'] = self.dados_tabela['Prevision Visitor'].round(2)
        self.dados_tabela['Prevision Home%'] = self.dados_tabela['Prevision Home%'].round(2)
        self.dados_tabela['Prevision Visitor%'] = self.dados_tabela['Prevision Visitor%'].round(2)

    def excluir_colunas(self):
        """Excluir as colunas do Brier"""
        self.dados_tabela = self.dados_tabela.drop(["BrierScore", "BrierScore%"], axis=1)

    def porcentagem(self):
        """colocar 'Prevision Home%' e 'Prevision Visitor%' em porcentagem"""
        self.dados_tabela['Prevision Visitor%'] = self.dados_tabela['Prevision Visitor%'].apply(lambda x: f"{x*100:.2f}%")
        self.dados_tabela['Prevision Home%'] = self.dados_tabela['Prevision Home%'].apply(lambda x: f"{x*100:.2f}%")

    def selecionar_datas(self):
        """Para os jogos que ainda não aconteceram, ou seja, que a linha de PTS Home estiver vazia
        Coloque o valor da linha anterior + 1"""
        self.dates = []
        for i in range(1, len(self.dados_tabela)):
            if pd.isna(self.dados_tabela.at[i, 'PTS Home']):
                self.dados_tabela.at[i, 'Número'] = self.dados_tabela.at[i - 1, 'Número'] + 1
                if self.dados_tabela.at[i, 'Número'] <= 15 and self.dados_tabela.at[i, 'Número'] != 0:
                    self.dates.append(self.dados_tabela.at[i, 'Número'])
            else:
                self.dados_tabela.at[i, 'Número'] = 0
        return print(f"{self.dates}")

class Dashboard(PrepararDados):
    """Dashboard que exibe os Dados"""
    def __init__(self):
        """variáveis chave da dashboard"""
        super().__init__()
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
        self.dados_tabela_filtrado = self.dados_tabela[self.dados_tabela["Número"].isin(self.dates)]
        self.layout()
    def layout(self):
        """Layout da Dashboard"""
        self.app.layout = html.Div(
            children=[
                dbc.Container(
                    fluid=True,
                    children=[
                        dbc.Row(
                            [
                                html.H1("PREVISÃO NBA", style={"color": "#f8f9fa"}),
                            ],
                            style={
                                "background-color": "#eb6864",
                                "color": "#f8f9fa",
                                "border": "2px solid #eb6864",
                                "border-radius": "5px",
                                "padding": "10px",
                                'textAlign': 'center',
                            },
                        ),
                        dbc.Row(style={'margin-bottom': '20px'}),
                        dash_table.DataTable(
                            id="tabela",
                            columns=[{'name': col, 'id': col} for col in self.dados_tabela_filtrado.columns],
                            data=self.dados_tabela_filtrado.to_dict("records"),
                            style_table={
                                "overflowY": "auto",
                                "font-family": "'News Cycle', 'Arial Narrow Bold', sans-serif",
                                "color": "#222",
                                "textAlign": "center",
                            },
                            style_header={
                                "backgroundColor": "#eb6864",
                                "color": "#222",
                                'textAlign': 'center',
                            },
                            style_cell={
                                "textAlign": "center",
                            },
                            style_data_conditional=[
                                {
                                    "if": {"column_id": "image"},
                                    "width": "10px",
                                    "height": "5px",
                                    "maxWidth": "10px",
                                    "maxHeight": "5px",
                                },
                            ],
                        ),
                    ],
                )
            ],
        )

    def rodardashboard(self):
        """executar porta"""
        return self.app.run_server(debug=False, port=8060)
