import random, time
from operator import itemgetter
from collections import defaultdict

class Cruzaold:
    def __init__(self, nome, linhas, colunas, palavras):
        self.nome = nome
        self.linhas = linhas
        self.colunas = colunas
        self.lista_palavras = palavras
        self.vazio = ' '
        self.coords_letra = defaultdict(list)

    def calcula_cruzada(self, tempo_permitido=1.00):
        self.melhor_listapalavras = []
        tam_listapalavras = len(self.lista_palavras)
        tempo_permitido = float(tempo_permitido)
        comeco_cheio = float(time.time())
        while (float(time.time()) - comeco_cheio) < tempo_permitido:
            self.prepara_palavra()
            [self.adiciona_palavra(palavra) for i in range(2) for palavra in self.lista_palavras
             if palavra not in self.atual_listapalavras]
            if len(self.atual_listapalavras) > len(self.melhor_listapalavras):
                self.melhor_listapalavras = list(self.atual_listapalavras)
                self.melhor_quadro = list(self.quadro)
            if len(self.melhor_listapalavras) == tam_listapalavras:
                break
        #answer = '\n'.join([''.join(['{} '.format(c) for c in self.best_grid[r]]) for r in range(self.rows)])
        resposta = '\n'.join([''.join([u'{} '.format(c) for c in self.melhor_quadro[r]])
                            for r in range(self.linhas)])
        return resposta + '\n\n' + str(len(self.melhor_listapalavras)) + ' out of ' + str(tam_listapalavras)
        
    
    def prepara_palavra(self):
        self.atual_listapalavras = []
        self.coords_letra.clear()
        self.quadro = [[self.vazio]*self.colunas for i in range(self.linhas)]
        self.lista_palavras = [palavra[:2] for palavra in self.lista_palavras]
        self.primeira_palavra(self.lista_palavras[0])

    def primeira_palavra(self, palavra):
        """Coloca a primeira palavra em uma posição aleatória no quadro."""
        vertical = random.randrange(0, 2)
        if vertical:
            linha = random.randrange(0, self.linhas - len(palavra[0]))
            coluna = random.randrange(0, self.colunas)
        else:
            linha = random.randrange(0, self.linhas)
            coluna = random.randrange(0, self.colunas - len(palavra[0]))
        self.set_palavra(palavra, linha, coluna, vertical)

    def adiciona_palavra(self, palavra):
        """Adiciona o restante das palavras no quadro."""
        lista_coords = self.get_coords(palavra)
        if not lista_coords:
            return
        linha, coluna, vertical = lista_coords[0], lista_coords[1], lista_coords[2]
        self.set_palavra(palavra, linha, coluna, vertical)

    def get_coords(self, palavra):
        """Retorna as coordenadas possíveis para cada letra."""
        tam_palavra = len(palavra[0])
        lista_coords = []
        lista_temp = [(l, v) for l, letra in enumerate(palavra[0])
                      for k, v in self.coords_letra.items() if k == letra]
        for coord in lista_temp:
            letc = coord[0]
            for item in coord[1]:
                (linhac, colc, vertc) = item
                if vertc:
                    if colc - letc >= 0 and (colc - letc) + tam_palavra <= self.colunas:
                        linha, coluna = (linhac, colc - letc)
                        pontos = self.checa_pontos_horiz(palavra, linha, coluna, tam_palavra)
                        if pontos:
                            lista_coords.append([linhac, colc - letc, 0, pontos])
                else:
                    if linhac - letc >= 0 and (linhac - letc) + tam_palavra <= self.linhas:
                        linha, coluna = (linhac - letc, colc)
                        pontos = self.checa_pontos_vert(palavra, linha, coluna, tam_palavra)
                        if pontos:
                            lista_coords.append([linhac - letc, colc, 1, pontos])
        if lista_coords:
            return max(lista_coords, key=itemgetter(3))
        else:
            return

    def checa_pontos_horiz(self, palavra, lin, col, tam_palavra, pontos=1):
        celula_ocupada = self.celula_ocupada
        if col and celula_ocupada(lin, col-1) or col + tam_palavra != self.colunas and celula_ocupada(lin, col + tam_palavra):
            return 0
        for letra in palavra[0]:
            celula_ativa = self.quadro[lin][col]
            if celula_ativa == self.vazio:
                if lin + 1 != self.linhas and celula_ocupada(lin+1, col) or lin and celula_ocupada(lin-1, col):
                    return 0
            elif celula_ativa == letra:
                pontos += 1
            else:
                return 0
            col += 1
        return pontos

    def checa_pontos_vert(self, palavra, lin, col, tam_palavra, pontos=1):
        celula_ocupada = self.celula_ocupada
        if lin and celula_ocupada(lin-1, col) or lin + tam_palavra != self.linhas and celula_ocupada(lin + tam_palavra, col):
            return 0
        for letra in palavra[0]:
            celula_ativa = self.quadro[lin][col]
            if celula_ativa == self.vazio:
                if col + 1 != self.colunas and celula_ocupada(lin, col+1) or col and celula_ocupada(lin, col-1):
                    return 0
            elif celula_ativa == letra:
                pontos += 1
            else:
                return 0
            lin += 1
        return pontos

    def set_palavra(self, palavra, linha, coluna, vertical):
        """Coloca palavras no quadro e adiciona-as à lista de palavras."""
        palavra.extend([linha, coluna, vertical])
        self.atual_listapalavras.append(palavra)

        horizontal = not vertical
        for letra in palavra[0]:
            self.quadro[linha][coluna] = letra
            if (linha, coluna, horizontal) not in self.coords_letra[letra]:
                self.coords_letra[letra].append((linha, coluna, vertical))
            else:
                self.coords_letra[letra].remove((linha, coluna, horizontal))
            if vertical:
                linha += 1
            else:
                coluna += 1

    def celula_ocupada(self, lin, col):
        celula = self.quadro[lin][col]
        if celula == self.vazio:
            return False
        else:
            return True

    def __str__(self):
        return str(self.linhas)