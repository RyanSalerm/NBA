from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from csv import DictWriter
from os import system
from datetime import datetime

system('cls')

class WebScraper:
    def __init__(self):
        self.fontes = ['https://www.basketball-reference.com/leagues/NBA_2024_games-october.html',
                       'https://www.basketball-reference.com/leagues/NBA_2024_games-november.html',
                       'https://www.basketball-reference.com/leagues/NBA_2024_games-december.html',
                       'https://www.basketball-reference.com/leagues/NBA_2024_games-january.html',
                       'https://www.basketball-reference.com/leagues/NBA_2024_games-february.html',
                       'https://www.basketball-reference.com/leagues/NBA_2024_games-march.html',
                       'https://www.basketball-reference.com/leagues/NBA_2024_games-april.html']
        print('Acessing... ')
        self.table_data_all = []  # Lista para armazenar os dados de todas as fontes
        self.table_data = []
        self.df = None
        self.cont = 0
        self.colunas_para_excluir = ['Arena', 'Notes', 'Attend.', '']
        self.df1 = None

    def scraper(self):
        for fonte in self.fontes:
            self.table_data_all = []
            response = get(fonte)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'class': 'stats_table'})
            self.cont += 1
            fonte_adicionada = False
            for row in table.find_all('tr'):
                row_data = []
                for cell in row.find_all(['th', 'td']):
                    row_data.append(cell.text.strip())
                if row_data:
                    self.table_data.append(row_data)
                    if row_data != "":
                        fonte_adicionada = True
            if fonte_adicionada:
                print(f'Fonte {self.cont} foi adicionada!')
            else:
                print(f'Fonte {self.cont} não foi adicionada!')
            self.table_data_all.extend(self.table_data[1:])  # Adiciona os dados, excluindo o cabeçalho, à lista geral
            self.df = pd.DataFrame(self.table_data_all, columns=self.table_data[0])

    def excluindo_colunas(self):
        self.df1 = self.df.drop(columns=self.colunas_para_excluir)
        print(self.df1.columns)
        print('DataFrame was create')
        novos_nomes_colunas = ['Date', 'Time', 'Visitor', 'PTS Visitor', 'Home', 'PTS Home']
        self.df1.columns = novos_nomes_colunas
        
    def salvar_csv(self):
        remover = "Date,Start (ET),Visitor/Neutral,PTS,Home/Neutral,PTS"

        with open('dados.csv', 'w') as arquivo:
            # Escrever o cabeçalho manualmente
            arquivo.write("Date,Time,Visitor,PTS Visitor,Home,PTS Home\n")

            # Iterar sobre as linhas do DataFrame para escrever no arquivo CSV
            for index, row in self.df1.iterrows():
                # Verificar se a linha atual é a linha a ser removida
                if ','.join(row.astype(str).values) == remover:
                    continue  # Pular a linha indesejada

                # Converter o formato da data
                formatted_date = datetime.strptime(row['Date'], "%a, %b %d, %Y").strftime("%Y-%m-%d")
                
                # Escrever a linha no arquivo CSV
                arquivo.write(f"{formatted_date},{row['Time']},{row['Visitor']},{row['PTS Visitor']},{row['Home']},{row['PTS Home']}\n")

