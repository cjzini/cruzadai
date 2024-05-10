import random, time
from operator import itemgetter
from collections import defaultdict

class Cruzada:
    def __init__(self, nome, linhas, colunas, palavras, palavras_ordenadas):
        self.nome = nome
        self.linhas = linhas
        self.colunas = colunas
        self.lista_palavras = palavras
        self.palavras_ordenadas = palavras_ordenadas
        self.lista_ordenada = {}
        self.quadro = [['.' for _ in range(self.linhas)] for _ in range(self.colunas)]
        self.coords_letra = defaultdict(list)
        self.palavras_adicionadas = {}
        self.vazio = '.'
        self.transforma_lista()

    def calcula_cruzada(self, tempo_permitido=1.00):
        self.melhor_listapalavras = []
        tam_listapalavras = len(self.lista_ordenada)
        tempo_permitido = float(tempo_permitido)
        tempo_comeco = float(time.time())
        while (float(time.time()) - tempo_comeco) < tempo_permitido:
            self.prepara_palavra()
            primeira_palavra = True
            # Iterando sobre o dicionário
            for chave, valores in self.lista_ordenada.items():
                palavra = []
                palavra.append((chave, valores))
                if primeira_palavra:
                    # Ignorar o primeiro item
                    primeira_palavra = False
                else:
                    if palavra[0][0] not in self.palavras_adicionadas:
                        self.adiciona_palavra(palavra[0])
            if len(self.palavras_adicionadas) > len(self.melhor_listapalavras):
                self.melhor_listapalavras = self.palavras_adicionadas
                self.melhor_quadro = list(self.quadro)
            if len(self.melhor_listapalavras) == tam_listapalavras:
                break
        self.imprime_quadro()
        self.imprime_listas()

    def transforma_lista(self):
        #self.lista_ordenada = [[chave, valor, 0] for chave, valor in self.palavras_ordenadas.items()]
        for chave, valor in self.palavras_ordenadas.items():
            lista_valores = [valor, 0]
            self.lista_ordenada[chave] = lista_valores
        #print(self.lista_ordenada)

    def prepara_palavra(self):
        self.palavras_adicionadas = {}
        self.coords_letra.clear()
        self.quadro = [['.' for _ in range(self.linhas)] for _ in range(self.colunas)]
        primeiro_elemento = next(iter(self.lista_ordenada.items()))
        self.primeira_palavra(primeiro_elemento)

    def primeira_palavra(self, palavra):
        """Coloca a primeira palavra em uma posição aleatória no quadro."""
        vertical = random.randrange(0, 2)
        if vertical:
            linha = random.randrange(0, self.linhas - len(palavra[0]))
            coluna = random.randrange(0, self.colunas)
        else:
            linha = random.randrange(0, self.linhas)
            coluna = random.randrange(0, self.colunas - len(palavra[0]))
        palavra[1][1] = vertical
        self.coloca_palavra(palavra, linha, coluna)

    def coloca_palavra(self, palavra, linha, coluna):
        """Coloca palavras no quadro e adiciona-as à lista de palavras."""
        palavra = list(palavra)
        vertical = palavra[1][1]
        horizontal = not vertical
        primeira_letra = None
        for letra in palavra[0]:
            if primeira_letra is None:
                primeira_letra = letra              
                tamanho_da_lista = len(palavra[1])
                if tamanho_da_lista == 2: # Armazena as coordenadas da primeira letra
                    palavra[1].append([primeira_letra, linha, coluna]) #Se ainda não existe, adiciona a coordenada
                else:
                    palavra[1][2] = [primeira_letra, linha, coluna] #Se ja existe, substitui a coordenada pois no final vai ficar a definitiva
            self.quadro[linha][coluna] = letra
            if (linha, coluna, horizontal) not in self.coords_letra[letra]:
                self.coords_letra[letra].append((linha, coluna, vertical))
            else:
                self.coords_letra[letra].remove((linha, coluna, horizontal))
            if vertical:
                linha += 1
            else:
                coluna += 1
        self.palavras_adicionadas[palavra[0]] = palavra[1]

    def adiciona_palavra(self, palavra):
        """Adiciona o restante das palavras no quadro."""
        lista_coords = self.pega_coords(palavra[0])
        if not lista_coords:
            return
        linha, coluna, vertical = lista_coords[0], lista_coords[1], lista_coords[2]
        palavra[1][1] = vertical
        self.coloca_palavra(palavra, linha, coluna)

    def pega_coords(self, palavra):
        """Retorna as coordenadas possíveis para cada letra."""
        tam_palavra = len(palavra)
        lista_coords = []
        lista_temp = [(l, v) for l, letra in enumerate(palavra)
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
        for letra in palavra:
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
        for letra in palavra:
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

    def celula_ocupada(self, lin, col):
        celula = self.quadro[lin][col]
        if celula == self.vazio:
            return False
        else:
            return True

    def imprime_quadro(self):
        for linha in self.melhor_quadro:
            print(''.join(map(str, linha)))
        #print(str(len(self.melhor_listapalavras)))
        print(self.melhor_listapalavras)

    def imprime_testes(self):
        lista_vertical = []
        lista_horizontal = []
        for i, (chave, valor) in enumerate(self.melhor_listapalavras.items(), 1):
            elemento = [i, chave, valor[0]]
            if valor[1] == 1:
                lista_vertical.append(elemento)
            else:
                lista_horizontal.append(elemento)
        print('Vertical:')
        for item in lista_vertical:
            print(item[0], item[1], item[2], '(' + str(len(item[1])) + ')')
        print('Horizontal:')  
        for item in lista_horizontal:
            print(item[0], item[1],item[2], '(' + str(len(item[1])) + ')')

    def imprime_listas(self):
        lista_vertical = []
        lista_horizontal = []

        # Adicionando números de ordem com base na posição de coluna e linha
        for i, (key, value) in enumerate(sorted(self.melhor_listapalavras.items(), key=lambda x: (x[1][2][1], x[1][2][2])), start=1):
            value.append(i)
            self.melhor_listapalavras[key] = value
            elemento = [i, key, value[0]]
            if value[1] == 1:
                lista_vertical.append(elemento)
            else:
                lista_horizontal.append(elemento)
          
        print('Vertical:')
        for item in lista_vertical:
            print(item[0], item[1], item[2], '(' + str(len(item[1])) + ')')
        print('Horizontal:')  
        for item in lista_horizontal:
            print(item[0], item[1],item[2], '(' + str(len(item[1])) + ')')

    def __str__(self):
        return (self.nome)