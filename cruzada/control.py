import os
import random

from cruzada.cruzada import Cruzada

base_dir = os.path.abspath(os.path.dirname(__file__))
#print(base_dir)
caminho = os.getcwd() + '/uploads/cruzada1.txt'
#print(caminho)

class Gerador:
    def __init__(self, caminho):
        self.caminho = os.getcwd() + caminho
        self.linhas = {}
        self.palavras_ordenadas = {}
        self.palavras = []
        self.pistas = []
        self.ler_arquivo()
        self.ordena_palavras()
        self.tamanho_quadro()

    def ler_arquivo(self):
        with open(self.caminho, 'r') as arquivo:
            for linha in arquivo:
                conteudo = linha.split(':')
                self.linhas[conteudo[0]] = conteudo[1].rstrip('\n')

    def ordena_palavras(self):
        self.palavras_ordenadas = dict(sorted(self.linhas.items(), key=lambda x: len(x[0]), reverse=True))
        self.palavras = list(self.palavras_ordenadas.keys())
        self.pistas = list(self.palavras_ordenadas.values())
    
    def tamanho_quadro(self):
        """Calcula o tamanho máximo do quadro."""
        if len(self.palavras) <= 20:
            self.nlin = self.ncol = len(self.palavras) + 3
        elif len(self.palavras) <= 100:
            self.nlin = self.ncol = int((round((len(self.palavras) - 20) / 8.0) * 2) + 19)
        else:
            self.nlin = self.ncol = 41
        if min(self.nlin, self.ncol) <= len(self.palavras[0]):
            self.nlin = self.ncol = len(self.palavras[0]) + 2

    def gera_quadro(self):
        cruzada = Cruzada('Teste', self.nlin, self.ncol, self.palavras, self.palavras_ordenadas)
        cruzada.calcula_cruzada()