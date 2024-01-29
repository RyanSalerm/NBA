"""Bibliotecas Necessárias"""
from web_scraping import WebScraper
from fitrar_csv import FiltrarDatas
from model import ModeloPreditivo
from dashboard import Dashboard

class Menu:
    """Menu do Programa"""
    def __init__(self):
        """Chama as funções no início"""
        self.web_scraping()
        self.filtrar_csv()
        self.preparandodados()
        self.dashboard()

    def web_scraping(self):
        """Pega os dados da NBA da web"""
        obj = WebScraper()
        obj.scraper()
        obj.excluindo_colunas()
        obj.salvar_csv()        

    def filtrar_csv(self):
        """Filtra eles por data"""
        filtro = FiltrarDatas()
        filtro.filtrar()
        filtro.salvar()

    def preparandodados(self):
        """atualiza a planilha, roda o modelo preditivo"""
        m = ModeloPreditivo()
        m.atualizando_a_planilha()
        #m.solver()
        m.adicionando_solucao()
        m.jogos()

    def dashboard(self):
        """roda a interface, que exibe as previsões"""
        run = Dashboard()
        run.layout()
        run.rodardashboard()

if __name__ == "__main__":
    run = Menu()
