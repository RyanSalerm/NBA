"""Bibliotecas Necessárias"""
import xlwings as xw
import pandas as pd
import numpy as np

class PreparandoDados:
    """Classe que prepara os dados"""
    def __init__(self):
        """Inicio"""
        self.dados = pd.read_csv('dados_filtrados.csv')
        self.df = pd.DataFrame(self.dados)
        self.df2 = pd.DataFrame()
        self.df3 = pd.DataFrame()
        self.remover_duplicatas()
        self.inicializar_df2()

    def remover_duplicatas(self):
        """Remove duplicatas"""
        self.df2['Teams'] = self.df['Home'].drop_duplicates()
        return self.df2['Teams']

    def inicializar_df2(self):
        """Inicializa o df2"""
        self.df2['Pontos Marcados Casa'] = 14
        self.df2['Pontos Sofridos Casa'] = 14
        self.df2['Pontos Marcados Fora'] = 14
        self.df2['Pontos Sofridos Fora'] = 14
        self.df2['Probabilidade Marcada Casa'] = 0.5
        self.df2['Probabilidade Sofrida Casa'] = 0.5
        self.df2['Probabilidade Marcada Fora'] = 0.5
        self.df2['Probabilidade Sofrida Fora'] = 0.5

    def somase(self, teams, condition, values):
        """Replica a fórmula somase do excel"""
        result = np.sum(np.where(teams == condition, values, 0))
        return float(result)


class ModeloPreditivo(PreparandoDados):
    """Pega os dados já organizados, através de uma herança"""
    def __init__(self):
        """Inicio"""
        super().__init__()
        self.wb = xw.Book("NBA.xlsm")
        self.atualizando_a_planilha()
        #self.solver()
        self.adicionando_solucao()
    def solver(self):
        """Solver"""
        macro_name = "Macro1"
        self.wb.macro(macro_name)
        self.wb.macro("Macro3")

        # Fechar o livro se necessário
        self.wb.save()  # Salva as alterações, se houver
        self.wb.close()
    def atualizando_a_planilha(self):
        """Atualizar planilha do Excel"""
        self.df.fillna(0, inplace=True)
        colunas_exportar = self.df[['Date', 'Time', 'Visitor', 'PTS Visitor', 'Home', 'PTS Home']]
        
        # Ajuste o índice de colunas_exportar para coincidir com o índice de self.df
        colunas_exportar.index = self.df.index
        
        sheet = self.wb.sheets[2]
        start_row = 1
        start_col = 1
        top_left_cell = sheet.cells(start_row, start_col)

        # Utilize o método value para escrever os dados
        top_left_cell.options(index=False, header=True).value = colunas_exportar
    def adicionando_solucao(self):
        """
        Obter valores diretamente da coluna C
        """
        pontos_marcados_casa = self.wb.sheets[0].range("C5:C34").value
        pontos_sofridos_casa = self.wb.sheets[0].range("D5:D34").value
        pontos_marcados_fora = self.wb.sheets[0].range("E5:E34").value
        pontos_sofridos_fora = self.wb.sheets[0].range("F5:F34").value
        probabilidade_marcada_casa = self.wb.sheets[1].range("C5:C34").value
        probabilidade_sofrida_casa = self.wb.sheets[1].range("D5:D34").value
        probabilidade_marcada_fora = self.wb.sheets[1].range("E5:E34").value
        probabilidade_sofrida_fora = self.wb.sheets[1].range("F5:F34").value
        times2 = self.wb.sheets[1].range("B5:B34").value
        times = self.wb.sheets[0].range("B5:B34").value
        self.df2['Teams'] = [t for t in times]
        self.df3['Teams2'] = [t for t in times2]
        if pontos_marcados_casa is not None:
            self.df2["Pontos Marcados Casa"] = [
                self.somase(self.df2['Teams'], t, pontos_marcados_casa)
                for t in self.df2['Teams']
            ]
            self.df2["Pontos Sofridos Casa"] = [
                self.somase(self.df2['Teams'], t, pontos_sofridos_casa)
                for t in self.df2['Teams']
            ]
            self.df2["Pontos Marcados Fora"] = [
                self.somase(self.df2['Teams'], t, pontos_marcados_fora)
                for t in self.df2['Teams']
            ]
            self.df2["Pontos Sofridos Fora"] = [
                self.somase(self.df2['Teams'], t, pontos_sofridos_fora)
                for t in self.df2['Teams']
            ]
            self.df3['Probabilidade Marcada Casa'] = [
                self.somase(self.df3['Teams2'], u, probabilidade_marcada_casa)
                for u in self.df3['Teams2']
            ]
            self.df3['Probabilidade Sofrida Casa'] = [
                self.somase(self.df3['Teams2'], u, probabilidade_sofrida_casa)
                for u in self.df3['Teams2']
            ]
            self.df3['Probabilidade Marcada Fora'] = [
                self.somase(self.df3['Teams2'], u, probabilidade_marcada_fora)
                for u in self.df3['Teams2']
            ]
            self.df3['Probabilidade Sofrida Fora'] = [
                self.somase(self.df3['Teams2'], u, probabilidade_sofrida_fora)
                for u in self.df3['Teams2']
            ]
        else:
            print("pontos_marcados_casa é None.")
        self.df['PTS Home'] = self.wb.sheets[0].range("M5:M1233").value
        self.df['PTS Visitor'] = self.wb.sheets[0].range("K5:K1233").value
        self.df['Prevision Home'] = self.wb.sheets[0].range("R5:R1233").value
        self.df['Prevision Visitor'] = (
            self.wb.sheets[0].range("S5:S1233").value
        )
        self.df['BrierScore'] = self.wb.sheets[0].range("T5:T1233").value
        self.df['Prevision Home%'] = self.wb.sheets[1].range("R5:R1233").value
        self.df['Prevision Visitor%'] = (
            self.wb.sheets[1].range("S5:S1233").value
        )
        self.df['BrierScore%'] = self.wb.sheets[1].range("T5:T1233").value
        self.df = pd.DataFrame(self.df)

    def solucao_probabilidades(self):
        """
        Imprime as probabilidades
        """
        return self.df3

    def solucao_pontos(self):
        """
        Imprime o segundo dataframe
        """
        return self.df2

    def jogos(self):
        """
        Imprime o DataFrame df contendo dados relacionados a jogos.
        """
        return self.df

    def aproveitamento(self):
        """
        Imprime o aproveitamento
        """
        apr_pontos = self.wb.sheets[0].range("V4").value
        prob = self.wb.sheets[1].range("V4").value

        return f"Apr. Pontos: {apr_pontos:.2%}, Apr. Probabilidade: {prob:.2%}"

