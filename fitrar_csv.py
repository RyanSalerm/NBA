"""Bibliotecas Necessárias"""
import pandas as pd

class FiltrarDatas:
    """Filtra as datas"""
    def __init__(self):
        """Inicia"""
        self.dados = pd.read_csv('dados.csv')
        self.data_inicio = '2023-10-24'
        self.data_final = '2024-04-14'
        self.filtro_data = None
        self.linhas_filtradas = None
        self.filtrar()
        self.salvar()
    def filtrar(self):
        """Filtra"""
        self.filtro_data = (self.dados['Date'] >= self.data_inicio) & (self.dados['Date'] <= self.data_final)
        self.linhas_filtradas = self.dados[self.filtro_data]
    def salvar(self):
        """salva"""
        self.linhas_filtradas.to_csv('dados_filtrados.csv', index=False)
